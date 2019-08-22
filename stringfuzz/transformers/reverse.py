'''
Reversing every string literal
'''

from stringfuzz.ast import StringLitNode, ConcatNode, ReConcatNode
from stringfuzz.ast_walker import ASTWalker
from stringfuzz.sf_vsfx import process_vsfx, VSFX_REVERSE

__all__ = [
    'reverse',
]

class ReverseTransformer(ASTWalker):
    def __init__(self, ast):
        super().__init__(ast)

    def exit_literal(self, literal, parent):
        if isinstance(literal, StringLitNode):
            literal.value = literal.value[::-1]

    def exit_expression(self, expr, parent):
        if isinstance(expr, (ConcatNode, ReConcatNode)):
            expr.body = reversed(expr.body)

# public API
def reverse(ast, vsfxpath, vstringfuzzx):
    if vstringfuzzx:
        transformed = process_vsfx(vsfxpath, ast, VSFX_REVERSE)
    else:
        transformed = ReverseTransformer(ast).walk()
    return transformed