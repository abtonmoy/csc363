import sys

from .AbstractASTVisitor import AbstractASTVisitor
from ...compiler.Scope import Scope


class TypeChecker(AbstractASTVisitor):

  def _err(self):
    print("TYPE ERROR", file=sys.stderr)
    sys.exit(7)

  def postprocessBinaryOpNode(self, node, left, right):
    lt = node.getLeft().getType()
    rt = node.getRight().getType()
    if lt != rt or lt not in (Scope.Type.INT, Scope.Type.FLOAT):
      self._err()

  def postprocessUnaryOpNode(self, node, expr):
    if node.getExpr().getType() not in (Scope.Type.INT, Scope.Type.FLOAT):
      self._err()

  def postprocessAssignNode(self, node, left, right):
    if node.getLeft().getType() != node.getRight().getType():
      self._err()

  def postprocessCondNode(self, node, left, right):
    if node.getLeft().getType() != node.getRight().getType():
      self._err()

  def postprocessCallNode(self, node, args):
    declared = node.ste.getArgTypes()
    actual = node.getArgs()
    if len(declared) != len(actual):
      self._err()
    for d, a in zip(declared, actual):
      if d != a.getType():
        self._err()

  def postprocessReturnNode(self, node, retExpr):
    if node.getFuncSymbol().getReturnType() != node.getRetExpr().getType():
      self._err()
