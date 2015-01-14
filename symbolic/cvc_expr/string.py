import logging

import CVC4

from .expression import CVCExpression
from .integer import CVCInteger

log = logging.getLogger("se.cvc.string")


class CVCString(CVCExpression):
    @classmethod
    def variable(cls, name, solver):
        em = solver.getExprManager()
        expr = em.mkVar(name, em.stringType())
        return cls(expr, solver)

    @classmethod
    def constant(cls, v, solver):
        em = solver.getExprManager()
        return cls(em.mkConst(CVC4.CVC4String(v)), solver)

    def getvalue(self):
        ce = self.solver.getValue(self.cvc_expr)
        return ce.getConstString().toString()

    def len(self):
        return CVCInteger(self.em.mkExpr(CVC4.STRING_LENGTH, self.cvc_expr), self.solver)