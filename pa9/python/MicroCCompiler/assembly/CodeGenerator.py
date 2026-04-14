import sys
import os

from .CodeObject import CodeObject
from .InstructionList import InstructionList
from .instructions import *
from ..compiler import *
from ..ast import *
from ..ast.visitor.AbstractASTVisitor import AbstractASTVisitor

class CodeGenerator(AbstractASTVisitor):

  def __init__(self):
    self.intRegCount = 1 # Changed from 0 so t0 is never used, this way maybe we could use t0 for the constant 0 register
    self.floatRegCount = 1 
    self.intTempPrefix = 't'
    self.floatTempPrefix = 'f'
    self.numCtrlStructs = 0



  def getIntRegCount(self):
    return self.intRegCount

  def getFloatRegCount(self):
    return self.floatRegCount

  # Generate code for Variables
  #
  # Create a code object that just holds a variable
  # Important: add a pointer from the code object to the symbol table entry so
  # we know how to generate code for it later (we'll need it to find the
  # address)
  #
  # Mark the code object as holding a variable, and also as an lval

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

    if var.type is Scope.Type.INT:
      temp = self.generateTemp(Scope.Type.INT)
      co.code.append(GetI(temp))
      address = self.generateAddrFromVariable(var)
      temp2 = self.generateTemp(Scope.Type.INT)
      co.code.append(La(temp2, address))
      co.code.append(Sw(temp, temp2, '0'))

    elif var.type is Scope.Type.FLOAT:
      temp = self.generateTemp(Scope.Type.FLOAT)
      co.code.append(GetF(temp))
      address = self.generateAddrFromVariable(var)
      temp2 = self.generateTemp(Scope.Type.INT)
      co.code.append(La(temp2, address))
      co.code.append(Fsw(temp, temp2, '0'))

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
      co.temp2 = 't0'
      if op in ('<', '<=', '=='):
        co.cmptype = 'fbeq'
      else:
        co.cmptype = 'fbne'
    else:
      raise Exception("Bad type in cond node")

    return co


  def postprocessIfStatementNode(self, node: IfStatementNode, cond: CodeObject, tlist: CodeObject, elist: CodeObject) -> CodeObject:
    self._incrnumCtrlStruct()
    labelnum = self._getnumCtrlStruct()

    co = CodeObject()

    elseLabel = self._generateElseLabel(labelnum)
    doneLabel = self._generateDoneLabel(labelnum)

    co.code.extend(cond.code)

    hasElse = (elist is not None)
    branchTarget = elseLabel if hasElse else doneLabel
    co.code.extend(self._makeBranch(cond, branchTarget))

    co.code.extend(tlist.code)

    if hasElse:
      co.code.append(J(doneLabel))
      co.code.append(Label(elseLabel))
      co.code.extend(elist.code)

    co.code.append(Label(doneLabel))

    co.lval = False
    co.type = None
    return co


  def postprocessWhileNode(self, node: WhileNode, cond: CodeObject, wlist: CodeObject) -> CodeObject:
    self._incrnumCtrlStruct()
    labelnum = self._getnumCtrlStruct()

    loopLabel = self._generateLoopLabel(labelnum)
    doneLabel = self._generateDoneLabel(labelnum)

    co = CodeObject()

    co.code.append(Label(loopLabel))
    co.code.extend(cond.code)
    co.code.extend(self._makeBranch(cond, doneLabel))
    co.code.extend(wlist.code)
    co.code.append(J(loopLabel))
    co.code.append(Label(doneLabel))

    co.lval = False
    co.type = None
    return co
  


  def postprocessReturnNode(self, node: ReturnNode, retExpr: CodeObject) -> CodeObject:
    co = CodeObject()

    if retExpr.lval is True:
      retExpr = self.rvalify(retExpr)

    co.code.extend(retExpr.code)
    co.code.append(Halt())
    co.type = None

    return co

  
  def generateTemp(self, t: Scope.Type) -> str:
    if t == Scope.Type.INT:
      s = self.intTempPrefix + str(self.intRegCount)
      self.intRegCount += 1
      return s
    elif t == Scope.Type.FLOAT:
      s = self.floatTempPrefix + str(self.floatRegCount)
      self.floatRegCount += 1
      return s
    else:
      raise Exception("Generating temp for bad type")

  


  def rvalify(self, lco : CodeObject) -> CodeObject:
    assert(lco.lval is True)
    assert(lco.isVar() is True)

    co = CodeObject()

    address = self.generateAddrFromVariable(lco)
    temp1 = self.generateTemp(Scope.Type.INT)   # Addresses are always ints
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
    address = symbol.addressToString()

    return address


# Here we should define functions that generate labels for conditionals and loops

  def _incrnumCtrlStruct(self):
    self.numCtrlStructs += 1

  def _getnumCtrlStruct(self) -> int:
    return self.numCtrlStructs
  
  def _generateThenLabel(self, num: int) -> str:
    return "then"+str(num)

  def _generateElseLabel(self, num: int) -> str:
    return "else"+str(num)

  def _generateLoopLabel(self, num: int) -> str:
    return "loop"+str(num)

  def _generateDoneLabel(self, num: int) -> str:
    return "done"+str(num)

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