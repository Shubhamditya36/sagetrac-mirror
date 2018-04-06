#*****************************************************************************
#       Copyright (C) 2009 Carl Witty <Carl.Witty@gmail.com>
#       Copyright (C) 2015 Jeroen Demeyer <jdemeyer@cage.ugent.be>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#                  http://www.gnu.org/licenses/
#*****************************************************************************

"""Base classes for interpreter specs."""

from __future__ import print_function, absolute_import

from ..memory import (MemoryChunkConstants, MemoryChunkArguments,
                      MemoryChunkScratch)
from ..storage import StorageTypeAssignable, ty_int


class InterpreterSpec(object):
    r"""
    Each interpreter to be generated by this module is represented
    by an InterpreterSpec.
    """

    name = ''

    def __init__(self):
        r"""
        Initialize an InterpreterSpec.

        Initializes the following fields:

        - ``c_header`` -- a code snippet to go at the top of the C
           interpreter source file
        - ``pxd_header`` -- a code snippet to go at the top of the
           wrapper class .pxd file
        - ``pyx_header`` -- a code snippet to go at the top of the
          wrapper class source file
        - ``err_return`` -- a string indicating the value to be
          returned in case of a Python exception
        - ``mc_code`` -- a memory chunk to use for the interpreted code
        - ``extra_class_members`` -- Class members for the wrapper that
          don't correspond to memory chunks
        - ``extra_members_initialize`` -- Code to initialize
          extra_class_members

        EXAMPLES::

            sage: from sage_setup.autogen.interpreters import *
            sage: interp = RDFInterpreter()
            sage: interp.c_header
            '#include <gsl/gsl_math.h>'
            sage: interp.pxd_header
            ''
            sage: interp.pyx_header
            'cimport sage.libs.gsl.math  # Add dependency on GSL'
            sage: interp.err_return
            '-1094648009105371'
            sage: interp.mc_code
            {MC:code}
            sage: interp = RRInterpreter()
            sage: interp.extra_class_members
            ''
            sage: interp.extra_members_initialize
            ''
        """
        self.c_header = ''
        self.pxd_header = ''
        self.pyx_header = ''
        self.err_return = 'NULL'
        self.mc_code = MemoryChunkConstants('code', ty_int)
        self.extra_class_members = ''
        self.extra_members_initialize = ''

    def _set_opcodes(self):
        r"""
        Assign opcodes to the instructions in this interpreter.

        Must be called at the end of __init__ by any subclass of
        InterpreterSpec.

        EXAMPLES::

            sage: from sage_setup.autogen.interpreters import *
            sage: interp = RDFInterpreter()
            sage: interp.instr_descs[5].opcode
            5
        """
        for i in range(len(self.instr_descs)):
            self.instr_descs[i].opcode = i


class StackInterpreter(InterpreterSpec):
    r"""
    A subclass of InterpreterSpec, specialized for stack-based
    interpreters.  (Currently all interpreters are stack-based.)
    """

    def __init__(self, type, mc_retval=None):
        r"""
        Initialize a StackInterpreter.

        INPUT:

        - type -- A StorageType; the basic type that this interpreter
          operates on
        - mc_retval -- default None; if not None, a special-purpose
          MemoryChunk to use as a return value

        Initializes the fields described in the documentation for
        InterpreterSpec.__init__, as well as the following:

        mc_args, mc_constants, mc_stack -- MemoryChunk values
        return_type -- the type returned by the C interpreter (None for int,
                       where 1 means success and 0 means error)
        mc_retval -- None, or the MemoryChunk to use as a return value
        ipow_range -- the range of exponents supported by the ipow
                      instruction (default is False, meaning never use ipow)
        adjust_retval -- None, or a string naming a function to call
                         in the wrapper's __call__ to modify the return
                         value of the interpreter
        implement_call_c -- True if the wrapper should have a fast cdef call_c
                            method (that bypasses the Python call overhead)
                            (default True)

        EXAMPLES::

            sage: from sage_setup.autogen.interpreters import *
            sage: rdf = RDFInterpreter()
            sage: rr = RRInterpreter()
            sage: el = ElementInterpreter()
            sage: rdf.mc_args
            {MC:args}
            sage: rdf.mc_constants
            {MC:constants}
            sage: rdf.mc_stack
            {MC:stack}
            sage: rr.mc_retval
            {MC:retval}
            sage: rr.return_type is None
            True
            sage: rdf.return_type.type
            'double'
            sage: rdf.implement_call_c
            True
            sage: el.implement_call_c
            False
        """
        super(StackInterpreter, self).__init__()
        self.mc_args = MemoryChunkArguments('args', type)
        self.mc_constants = MemoryChunkConstants('constants', type)
        self.mc_stack = MemoryChunkScratch('stack', type, is_stack=True)
        if isinstance(type, StorageTypeAssignable):
            self.return_type = type
        else:
            self.return_type = None
        self.mc_retval = mc_retval
        self.ipow_range = False
        self.adjust_retval = None
        self.implement_call_c = True
