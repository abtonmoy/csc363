import sys
import os
from typing import List

from .CodeObject import CodeObject
from .InstructionList import InstructionList
from .instructions import *
from ..compiler import *
from ..ast import *
from ..ast.visitor.AbstractASTVisitor import AbstractASTVisitor

class CodeGenerator(AbstractASTVisitor):

  def __init__(self):
    self.intRegCount = 0
    self.floatRegCount = 0
    self.intTempPrefix = 't'
    self.floatTempPrefix = 'f'
    self.loopLabel = 0
    self.elseLabel = 0
    self.outLabel = 0
    self.currFunc = None

  def getIntRegCount(self):
    return self.intRegCount

  def getFloatRegCount(self):
    return self.floatRegCount

  def postprocessVarNode(self, node: VarNode) -> CodeObject:
    sym = node.getSymbol()
    co = CodeObject(sym)
    co.lval = True
    co.type = node.getType()
    return co

  def postprocessIntLitNode(self, node: IntLitNode) -> CodeObject:
    co = CodeObject()
    temp = self.generateTemp(Scope.Type.INT)
    val = node.getVal()
    co.code.append(Li(temp, val))
    co.temp = temp
    co.lval = False
    co.type = node.getType()
    return co

  def postprocessFloatLitNode(self, node: FloatLitNode) -> CodeObject:
    co = CodeObject()
    temp = self.generateTemp(Scope.Type.FLOAT)
    val = node.getVal()
    co.code.append(FImm(temp, val))
    co.temp = temp
    co.lval = False
    co.type = node.getType()
    return co

  def postprocessBinaryOpNode(self, node: BinaryOpNode, left: CodeObject, right: CodeObject) -> CodeObject:
    co = CodeObject()

    if left.lval:
      left = self.rvalify(left)
    co.code.extend(left.code)

    if right.lval:
      right = self.rvalify(right)
    co.code.extend(right.code)

    op = node.getOp()
    resultType = left.type

    if resultType == Scope.Type.INT:
      temp = self.generateTemp(Scope.Type.INT)
      if op == BinaryOpNode.OpType.ADD:
        co.code.append(Add(left.temp, right.temp, temp))
      elif op == BinaryOpNode.OpType.SUB:
        co.code.append(Sub(left.temp, right.temp, temp))
      elif op == BinaryOpNode.OpType.MUL:
        co.code.append(Mul(left.temp, right.temp, temp))
      elif op == BinaryOpNode.OpType.DIV:
        co.code.append(Div(left.temp, right.temp, temp))
      else:
        raise Exception("Unknown binary op for INT")
    elif resultType == Scope.Type.FLOAT:
      temp = self.generateTemp(Scope.Type.FLOAT)
      if op == BinaryOpNode.OpType.ADD:
        co.code.append(FAdd(left.temp, right.temp, temp))
      elif op == BinaryOpNode.OpType.SUB:
        co.code.append(FSub(left.temp, right.temp, temp))
      elif op == BinaryOpNode.OpType.MUL:
        co.code.append(FMul(left.temp, right.temp, temp))
      elif op == BinaryOpNode.OpType.DIV:
        co.code.append(FDiv(left.temp, right.temp, temp))
      else:
        raise Exception("Unknown binary op for FLOAT")
    else:
      raise Exception("Bad type in binary op node")

    co.temp = temp
    co.lval = False
    co.type = resultType

    return co

  def postprocessUnaryOpNode(self, node: UnaryOpNode, expr: CodeObject) -> CodeObject:
    co = CodeObject()

    if expr.lval:
      expr = self.rvalify(expr)
    co.code.extend(expr.code)

    if expr.type == Scope.Type.INT:
      temp = self.generateTemp(Scope.Type.INT)
      co.code.append(Neg(src=expr.temp, dest=temp))
    elif expr.type == Scope.Type.FLOAT:
      temp = self.generateTemp(Scope.Type.FLOAT)
      co.code.append(FNeg(src=expr.temp, dest=temp))
    else:
      raise Exception("Non int/float type in unary op!")

    co.type = expr.type
    co.temp = temp
    co.lval = False
    return co

  def postprocessAssignNode(self, node: AssignNode, left: CodeObject, right: CodeObject) -> CodeObject:
    co = CodeObject()

    if right.lval:
      right = self.rvalify(right)
    co.code.extend(right.code)

    sym = left.getSTE()
    if sym.isLocal():
      offset = sym.addressToString()
      if left.type == Scope.Type.INT:
        co.code.append(Sw(right.temp, "fp", offset))
      elif left.type == Scope.Type.FLOAT:
        co.code.append(Fsw(right.temp, "fp", offset))
      else:
        raise Exception("Bad type in assign node")
    else:
      address = self.generateAddrFromVariable(left)
      addrTemp = self.generateTemp(Scope.Type.INT)
      co.code.append(La(addrTemp, address))
      if left.type == Scope.Type.INT:
        co.code.append(Sw(right.temp, addrTemp, '0'))
      elif left.type == Scope.Type.FLOAT:
        co.code.append(Fsw(right.temp, addrTemp, '0'))
      else:
        raise Exception("Bad type in assign node")

    co.lval = False
    co.type = None
    return co

  def postprocessStatementListNode(self, node: StatementListNode, statements: list) -> CodeObject:
    co = CodeObject()
    for subcode in statements:
      co.code.extend(subcode.code)
    co.type = None
    return co

  def postprocessReadNode(self, node: ReadNode, var: CodeObject) -> CodeObject:
    co = CodeObject()
    assert(var.isVar())

    sym = var.getSTE()

    if var.type is Scope.Type.INT:
      temp = self.generateTemp(Scope.Type.INT)
      co.code.append(GetI(temp))
      if sym.isLocal():
        co.code.append(Sw(temp, "fp", sym.addressToString()))
      else:
        addrTemp = self.generateTemp(Scope.Type.INT)
        co.code.append(La(addrTemp, sym.addressToString()))
        co.code.append(Sw(temp, addrTemp, '0'))
    elif var.type is Scope.Type.FLOAT:
      temp = self.generateTemp(Scope.Type.FLOAT)
      co.code.append(GetF(temp))
      if sym.isLocal():
        co.code.append(Fsw(temp, "fp", sym.addressToString()))
      else:
        addrTemp = self.generateTemp(Scope.Type.INT)
        co.code.append(La(addrTemp, sym.addressToString()))
        co.code.append(Fsw(temp, addrTemp, '0'))
    else:
      raise Exception("Bad type in read node")

    return co

  def postprocessWriteNode(self, node: WriteNode, expr: CodeObject) -> CodeObject:
    co = CodeObject()

    if expr.type == Scope.Type.STRING:
      address = self.generateAddrFromVariable(expr)
      addrTemp = self.generateTemp(Scope.Type.INT)
      co.code.append(La(addrTemp, address))
      co.code.append(PutS(addrTemp))
    elif expr.type == Scope.Type.INT:
      if expr.lval:
        expr = self.rvalify(expr)
      co.code.extend(expr.code)
      co.code.append(PutI(expr.temp))
    elif expr.type == Scope.Type.FLOAT:
      if expr.lval:
        expr = self.rvalify(expr)
      co.code.extend(expr.code)
      co.code.append(PutF(expr.temp))
    else:
      raise Exception("Bad type in write node")

    co.lval = False
    co.type = None
    return co

  def postprocessCondNode(self, node: CondNode, left: CodeObject, right: CodeObject) -> CodeObject:
    co = CodeObject()

    if left.lval:
      left = self.rvalify(left)
    co.code.extend(left.code)

    if right.lval:
      right = self.rvalify(right)
    co.code.extend(right.code)

    op = node.getOp()
    rev_op = self._reverseOpString(op)

    if left.type == Scope.Type.INT:
      co.temp = left.temp
      co.temp2 = right.temp
      co.cmptype = rev_op
    elif left.type == Scope.Type.FLOAT:
      cmpTemp = self.generateTemp(Scope.Type.INT)

      if op in ('<', '>='):
        co.code.append(Flt(left.temp, right.temp, cmpTemp))
      elif op in ('<=', '>'):
        co.code.append(Fle(left.temp, right.temp, cmpTemp))
      elif op in ('==', '!='):
        co.code.append(Feq(left.temp, right.temp, cmpTemp))
      else:
        raise Exception("Unknown float cmp op: " + str(op))

      co.temp = cmpTemp
      co.temp2 = 'x0'
      if op in ('<', '<=', '=='):
        co.cmptype = 'fbeq'
      else:
        co.cmptype = 'fbne'
    else:
      raise Exception("Bad type in cond node")

    return co

  def postprocessIfStatementNode(self, node: IfStatementNode, cond: CodeObject, tlist: CodeObject, elist: CodeObject) -> CodeObject:
    co = CodeObject()

    self.elseLabel += 1
    self.outLabel += 1
    elseLabelStr = "else_" + str(self.elseLabel)
    outLabelStr = "out_" + str(self.outLabel)

    co.code.extend(cond.code)

    hasElse = (elist is not None)
    branchTarget = elseLabelStr if hasElse else outLabelStr
    co.code.extend(self._makeBranch(cond, branchTarget))

    co.code.extend(tlist.code)

    if hasElse:
      co.code.append(J(outLabelStr))
      co.code.append(Label(elseLabelStr))
      co.code.extend(elist.code)

    co.code.append(Label(outLabelStr))

    co.lval = False
    co.type = None
    return co

  def postprocessWhileNode(self, node: WhileNode, cond: CodeObject, wlist: CodeObject) -> CodeObject:
    co = CodeObject()

    self.loopLabel += 1
    self.outLabel += 1
    loopLabelStr = "loop_" + str(self.loopLabel)
    outLabelStr = "out_" + str(self.outLabel)

    co.code.append(Label(loopLabelStr))
    co.code.extend(cond.code)
    co.code.extend(self._makeBranch(cond, outLabelStr))
    co.code.extend(wlist.code)
    co.code.append(J(loopLabelStr))
    co.code.append(Label(outLabelStr))

    co.lval = False
    co.type = None
    return co

  def postprocessReturnNode(self, node: ReturnNode, retExpr: CodeObject) -> CodeObject:
    co = CodeObject()

    if retExpr.lval:
      retExpr = self.rvalify(retExpr)
    co.code.extend(retExpr.code)

    if retExpr.type == Scope.Type.INT:
      co.code.append(Sw(retExpr.temp, "fp", "8"))
    elif retExpr.type == Scope.Type.FLOAT:
      co.code.append(Fsw(retExpr.temp, "fp", "8"))
    else:
      raise Exception("Bad return type")

    co.code.append(J(self._generateFunctionRetLabel()))
    co.type = None
    return co

  def preprocessFunctionNode(self, node: FunctionNode):
    self.currFunc = node.getFuncName()
    self.intRegCount = 0
    self.floatRegCount = 0

  def postprocessFunctionNode(self, node: FunctionNode, body: CodeObject) -> CodeObject:
    co = CodeObject()

    co.code.append(Label(self._generateFunctionLabel()))
    co.code.append(Sw("fp", "sp", "0"))
    co.code.append(Mv("sp", "fp"))
    co.code.append(Addi("sp", "-4", "sp"))

    numLocals = node.getScope().getNumLocals()
    co.code.append(Addi("sp", str(-4 * numLocals), "sp"))

    nInt = self.intRegCount
    nFloat = self.floatRegCount

    for i in range(1, nInt + 1):
      co.code.append(Sw(self.intTempPrefix + str(i), "sp", "0"))
      co.code.append(Addi("sp", "-4", "sp"))
    for i in range(1, nFloat + 1):
      co.code.append(Fsw(self.floatTempPrefix + str(i), "sp", "0"))
      co.code.append(Addi("sp", "-4", "sp"))

    co.code.extend(body.code)

    co.code.append(Label(self._generateFunctionRetLabel()))

    for i in range(nFloat, 0, -1):
      co.code.append(Addi("sp", "4", "sp"))
      co.code.append(Flw(self.floatTempPrefix + str(i), "sp", "0"))
    for i in range(nInt, 0, -1):
      co.code.append(Addi("sp", "4", "sp"))
      co.code.append(Lw(self.intTempPrefix + str(i), "sp", "0"))

    co.code.append(Mv("fp", "sp"))
    co.code.append(Lw("fp", "fp", "0"))
    co.code.append(Ret())

    return co

  def postprocessFunctionListNode(self, node: FunctionListNode, functions: List[CodeObject]) -> CodeObject:
    co = CodeObject()

    co.code.append(Mv("sp", "fp"))
    co.code.append(Jr(self._generateFunctionLabel("main")))
    co.code.append(Halt())
    co.code.append(Blank())

    for c in functions:
      co.code.extend(c.code)
      co.code.append(Blank())

    return co

  def postprocessCallNode(self, node: CallNode, args: List[CodeObject]) -> CodeObject:
    co = CodeObject()

    for arg in args:
      if arg.lval:
        arg = self.rvalify(arg)
      co.code.extend(arg.code)
      if arg.type == Scope.Type.INT:
        co.code.append(Sw(arg.temp, "sp", "0"))
      elif arg.type == Scope.Type.FLOAT:
        co.code.append(Fsw(arg.temp, "sp", "0"))
      else:
        raise Exception("Bad arg type")
      co.code.append(Addi("sp", "-4", "sp"))

    co.code.append(Addi("sp", "-4", "sp"))
    co.code.append(Sw("ra", "sp", "0"))
    co.code.append(Addi("sp", "-4", "sp"))

    co.code.append(Jr(self._generateFunctionLabel(node.getFuncName())))

    co.code.append(Addi("sp", "4", "sp"))
    co.code.append(Lw("ra", "sp", "0"))
    co.code.append(Addi("sp", "4", "sp"))

    retType = node.ste.getReturnType()
    if retType == Scope.Type.INT:
      retTemp = self.generateTemp(Scope.Type.INT)
      co.code.append(Lw(retTemp, "sp", "0"))
    elif retType == Scope.Type.FLOAT:
      retTemp = self.generateTemp(Scope.Type.FLOAT)
      co.code.append(Flw(retTemp, "sp", "0"))
    else:
      retTemp = None

    if len(args) > 0:
      co.code.append(Addi("sp", str(4 * len(args)), "sp"))

    co.temp = retTemp
    co.lval = False
    co.type = retType
    return co

  def generateTemp(self, t: Scope.Type) -> str:
    if t == Scope.Type.INT:
      self.intRegCount += 1
      return self.intTempPrefix + str(self.intRegCount)
    elif t == Scope.Type.FLOAT:
      self.floatRegCount += 1
      return self.floatTempPrefix + str(self.floatRegCount)
    else:
      raise Exception("Generating temp for bad type")

  def rvalify(self, lco: CodeObject) -> CodeObject:
    assert(lco.lval is True)
    assert(lco.isVar() is True)

    co = CodeObject()
    sym = lco.getSTE()

    if sym.isLocal():
      offset = sym.addressToString()
      if lco.type is Scope.Type.INT:
        temp2 = self.generateTemp(Scope.Type.INT)
        co.code.append(Lw(temp2, "fp", offset))
      elif lco.type is Scope.Type.FLOAT:
        temp2 = self.generateTemp(Scope.Type.FLOAT)
        co.code.append(Flw(temp2, "fp", offset))
      else:
        raise Exception("Bad local type in rvalify")
    else:
      address = self.generateAddrFromVariable(lco)
      temp1 = self.generateTemp(Scope.Type.INT)
      co.code.append(La(temp1, address))

      if lco.type is Scope.Type.INT:
        temp2 = self.generateTemp(Scope.Type.INT)
        co.code.append(Lw(temp2, temp1, '0'))
      elif lco.type is Scope.Type.FLOAT:
        temp2 = self.generateTemp(Scope.Type.FLOAT)
        co.code.append(Flw(temp2, temp1, '0'))
      elif lco.type is Scope.Type.STRING:
        temp2 = temp1
      else:
        raise Exception("Bad type in rvalify!")

    co.type = lco.type
    co.lval = False
    co.temp = temp2
    return co

  def generateAddrFromVariable(self, lco: CodeObject) -> str:
    assert(lco.isVar() is True)
    symbol = lco.getSTE()
    return symbol.addressToString()

  def _reverseOpString(self, op: str) -> str:
    reversals = {
      '<':  '>=',
      '<=': '>',
      '>':  '<=',
      '>=': '<',
      '==': '!=',
      '!=': '==',
    }
    if op not in reversals:
      raise Exception("Unknown operator in _reverseOpString: " + str(op))
    return reversals[op]

  def _makeBranch(self, cond: CodeObject, label: str) -> list:
    instructions = InstructionList()
    rev = cond.cmptype

    if rev == 'fbeq':
      instructions.append(Beq(cond.temp, cond.temp2, label))
    elif rev == 'fbne':
      instructions.append(Bne(cond.temp, cond.temp2, label))
    elif rev == '<':
      instructions.append(Blt(cond.temp, cond.temp2, label))
    elif rev == '<=':
      instructions.append(Ble(cond.temp, cond.temp2, label))
    elif rev == '>':
      instructions.append(Bgt(cond.temp, cond.temp2, label))
    elif rev == '>=':
      instructions.append(Bge(cond.temp, cond.temp2, label))
    elif rev == '==':
      instructions.append(Beq(cond.temp, cond.temp2, label))
    elif rev == '!=':
      instructions.append(Bne(cond.temp, cond.temp2, label))
    else:
      raise Exception("Unknown reversed op in _makeBranch: " + str(rev))

    return instructions

  def _generateFunctionLabel(self, func=None) -> str:
    if func is None:
      return "func_" + self.currFunc
    else:
      return "func_" + func

  def _generateFunctionRetLabel(self) -> str:
    return "func_ret_" + self.currFunc
