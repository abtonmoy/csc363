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
    self.intRegCount = 1
    self.floatRegCount = 1
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

  
  def postprocessIntLitNode(self, node: IntLitNode) -> CodeObject:


  def postprocessFloatLitNode(self, node: FloatLitNode) -> CodeObject:


  def postprocessBinaryOpNode(self, node: BinaryOpNode, left: CodeObject, right: CodeObject) -> CodeObject:



  def postprocessUnaryOpNode(self, node: UnaryOpNode, expr: CodeObject) -> CodeObject:



  def postprocessAssignNode(self, node: AssignNode, left: CodeObject, right: CodeObject) -> CodeObject:



  def postprocessStatementListNode(self, node: StatementListNode, statements: list) -> CodeObject:



  def postprocessReadNode(self, node: ReadNode, var: CodeObject) -> CodeObject:



  def postprocessWriteNode(self, node: WriteNode, expr: CodeObject) -> CodeObject:

	
  def postprocessCondNode(self, node: CondNode, left: CodeObject, right: CodeObject) -> CodeObject:


  def postprocessIfStatementNode(self, node: IfStatementNode, cond: CodeObject, tlist: CodeObject, elist: CodeObject) -> CodeObject:


  def postprocessWhileNode(self, node: WhileNode, cond: CodeObject, wlist:
  CodeObject) -> CodeObject:


  def postprocessReturnNode(self, node: ReturnNode, retExpr: CodeObject) -> CodeObject:
    '''
    This is responsible for handing things like "return b" or "return".  
    Notably, this part will NOT generate a RET instruction.
    Step 1: rvalify (if necessary) code for the retExpr
    Step 2: add in retExpr code
    Step 3: store return value from retExpr's temporary to the return value spot in the stack (8 up from FP)
    '''


  def preprocessFunctionNode(self, node: FunctionNode):

    self.currFunc = node.getFuncName()

    self.intRegCount = 1
    self.floatRegCount = 1


  def postprocessFunctionNode(self, node: FunctionNode, body: CodeObject) -> CodeObject:
    '''
    Responsible for actually putting together a function's code
    Step 1: Set up stack frame
    Step 2: Save temporaries
    Step 3: Add in body code (this will include a return node)
    Step 4: Load temporaries
    Step 5: Undo stack frame
    Step 6: Append the RET instruction
    '''

    co = CodeObject()



    return co


	

  def postprocessFunctionListNode(self, node: FunctionListNode, functions: List[CodeObject]) -> CodeObject:
    '''
    Generate code for the list of functions. This is the "top level" code generation function
    Step 1: Set fp to point to sp
    Step 2: Insert a JR to main
    Step 3: Insert a HALT
    Step 4: Include all the code of the functions
    '''

    co = CodeObject()

    co.code.append(Mv("sp", "fp"))
    co.code.append(Jr(self.generateFunctionEntryLabel("main")))
    co.code.append(Halt())
    co.code.append(Blank())

    # Add code for each of the functions
    for c in functions:
      co.code.extend(c.code)
      co.code.append(Blank())
    
    return co


  def postprocessCallNode(self, node: CallNode, args: List[CodeObject]) -> CodeObject:
    '''
    Responsible for handling when we actually make a function call, for example, something like a = foo(b)
    The call node would be the foo(b) call.
    Step 1: For each argument, insert rvalified code object and push result to stack
    Step 2: Allocate space for return value (what if there isn't one?)
    Step 3: Push ra to stack
    Step 4: JR to function
    Step 5: Pop ra back from stack
    Step 6: Pop return value into fresh temporary
    Step 7: Remove arguments from stack (move sp up, no need to keep these values)
    '''

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
 


  def generateAddrFromVariable(self, lco: CodeObject) -> str:
 


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
  


  
  def generateFunctionEntryLabel(self, func = None) -> str:
    if func is None:
      return "func_entry_" + self.currFunc
    else:
      return "func_entry_" + func
    
  def generateFunctionCodeLabel(self, func = None) -> str:
    if func is None:
      return "func_code_" + self.currFunc
    else:
      return "func_code_" + func  


  def generateFunctionRetLabel(self) -> str:
    return "func_ret_" + self.currFunc