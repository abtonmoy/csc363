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
    self.intRegCount = 0
    self.floatRegCount = 0
    self.intTempPrefix = 't'
    self.floatTempPrefix = 'f'

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
    # LI t2, 5
    co.code.append(Li(temp, val))
    co.temp = temp
    co.lval = False
    co.type = node.getType()


    return co


  def postprocessFloatLitNode(self, node: FloatLitNode) -> CodeObject:

    co = CodeObject()

    return co



  def postprocessBinaryOpNode(self, node: BinaryOpNode, left: CodeObject, right: CodeObject) -> CodeObject:

    co = CodeObject()


    return co



  def postprocessUnaryOpNode(self, node: UnaryOpNode, expr: CodeObject) -> CodeObject:
    '''
    Unary Op Node would be telling us to do -(expr)
    '''

    co = CodeObject()  # Step 0

    exprcode = expr.code # Add in all the code required to get expr
    
    if expr.lval:
      


    if expr.type == Scope.Type.INT:
      temp = self.generateTemp(Scope.Type.INT)
      co.code.append(Neg(src=expr.temp, dest=temp))
      

    elif expr.type == Scope.Type.FLOAT:

    else:
      raise Exception("Non int/float in unary op!")


    return co
  






  def postprocessAssignNode(self, node: AssignNode, left: CodeObject, right: CodeObject) -> CodeObject:
    co = CodeObject()


    return co



  def postprocessStatementListNode(self, node: StatementListNode, statements: list) -> CodeObject:
    co = CodeObject()

    for subcode in statements:
      co.code.extend(subcode.code)

    co.type = None
    return co


	
  def postprocessReadNode(self, node: ReadNode, var: CodeObject) -> CodeObject:

    co = CodeObject()


    return co


  def postprocessWriteNode(self, node: WriteNode, expr: CodeObject) -> CodeObject:

    co = CodeObject()

    return co

  
  def postprocessReturnNode(self, node: ReturnNode, retExpr: CodeObject) -> CodeObject:

    co = CodeObject()


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

    co = CodeObject()

    return co






  def generateAddrFromVariable(self, lco: CodeObject) -> CodeObject:

    co = CodeObject()


    return co
  
