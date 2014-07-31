#
# Copyright (c) 2011, EPFL (Ecole Politechnique Federale de Lausanne)
# All rights reserved.
#
# Created by Marco Canini, Daniele Venzano, Dejan Kostic, Jennifer Rexford
#
# Updated by Thomas Ball (2014)
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   -  Redistributions of source code must retain the above copyright notice,
#      this list of conditions and the following disclaimer.
#   -  Redistributions in binary form must reproduce the above copyright notice,
#      this list of conditions and the following disclaimer in the documentation
#      and/or other materials provided with the distribution.
#   -  Neither the names of the contributors, nor their associated universities or
#      organizations may be used to endorse or promote products derived from this
#      software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
# SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

import ast
import sys
from . symbolic_type import SymbolicType

def correct(value, bits, signed):
    base = 1 << bits 
    value %= base
    return value - base if signed and value.bit_length() == bits else value

# this models 32-bit word semantics (as in C)
# truncate = lambda v: correct(v, 32, True)

# this models Python integer semantics
truncate = lambda v : v

# we use multiple inheritance to achieve concrete execution for any
# operation for which we don't have a symbolic representation. As
# we can see a SymbolicInteger is both symbolic (SymbolicType) and 
# concrete (int)

class SymbolicInteger(SymbolicType,int):
	def __new__(cls, name, v, expr=None):
		return int.__new__(cls, v)

	def __init__(self, name, v, expr=None):
		SymbolicType.__init__(self, name, expr)
		self.val = v

	def wrap(self,conc,sym):
		return SymbolicInteger("se",conc,sym)
	
	# we must ensure that we are no longer inheriting from SymbolicType
	def getConcrValue(self):
		return self.val

	def __add__(self, other):
		return self._do_bin_op(other, lambda x, y: truncate(x+y), ast.Add)
	def __radd__(self,other):
		return self.__add__(other)

	def __sub__(self, other):
		return self._do_bin_op(other, lambda x, y: truncate(x - y), ast.Sub)
	def __rsub__(self,other):
		return self.__sub__(other)

	def __mul__(self, other):
		return self._do_bin_op(other, lambda x, y: truncate(x*y), ast.Mult)
	def __rmul__(self,other):
		return self.__mul__(other)

	def __mod__(self, other):
		return self._do_bin_op(other, lambda x, y: truncate(x % y), ast.Mod)
	def __rmod__(self,other):
		return self.__mod__(other)

	def __div__(self, other):
		return self._do_bin_op(other, lambda x, y: truncate(x / y), ast.Div)
	def __rdiv__(self,other):
		return self.__div__(other)

	# bit level operations

	def __and__(self, other):
		return self._do_bin_op(other, lambda x, y: truncate(x & y), ast.BitAnd)
	def __rand__(self,other):
		return self.__and__(other)

	def __or__(self, other):
		return self._do_bin_op(other, lambda x, y: truncate(x | y), ast.BitOr)
	def __ror__(self,other):
		return self.__or__(other)

	def __xor__(self, other):
		return self._do_bin_op(other, lambda x, y: truncate(x ^ y), ast.BitXor)
	def __rxor__(self,other):
		return self.__xor__(other)

	def __lshift__(self, other):
		return self._do_bin_op(other, lambda x, y: truncate(x << y), ast.LShift)
	def __rlshift__(self,other):
		return self.__lshift__(other)

	def __rshift__(self, other):
		return self._do_bin_op(other, lambda x, y: truncate(x >> y), ast.RShift)
	def __rrshift__(self,other):
		return self.__rshift__(other)

	# no symbolic implementation for
	#
	# __floordiv__
	# __divmod__
	# __pow__
	# __bit_length__

