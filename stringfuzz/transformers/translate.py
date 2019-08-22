'''
Permuting the alphabet in every string literal.
'''

import random
import copy

from stringfuzz.sf_vsfx import process_vsfx, VSFX_TRANSLATE
from stringfuzz.ast import StringLitNode, ReRangeNode
from stringfuzz.ast_walker import ASTWalker
from stringfuzz.generator import generate
from stringfuzz import ALL_CHARS
from stringfuzz.constants import SMT_25_STRING

__all__ = [
    'translate'
]

WITH_INTEGERS    = list(ALL_CHARS)
WITHOUT_INTEGERS = [c for c in ALL_CHARS if not c.isdecimal()]

def _replace_escchar(str_repl: str):
    repl_map = {
        '\n': '\\n',
        '\t': '\\t',
        '\"': '\\"',
        '\r': '\\r'
    }
    for key, val in repl_map.items():
        str_repl = str_repl.replace(key, val)
    return str_repl
class StringShuffler:
    """ Representation for Shuffler function of strings.
    """
    def __init__(self, character_set):
        shuffled_list = copy.copy(character_set)
        random.shuffle(shuffled_list)
        self.shuffled = ''.join(shuffled_list)
        self.character_set = ''.join(character_set)

    def get_table(self):
        return str.maketrans(self.character_set, self.shuffled)

    def get_sexpr(self) -> str:
        return '("{0}" "{1}")'.format(_replace_escchar(self.character_set), _replace_escchar(self.shuffled))
    
    def get_charpair(self) -> list:
        return [self.character_set, self.shuffled]


class TranslateTransformer(ASTWalker):
    def __init__(self, ast, shuffler, skip_re_range):
        super().__init__(ast)
        self.shuffler = shuffler
        self.table = self.shuffler.get_table()
        self.skip_re_range = skip_re_range

    def exit_literal(self, literal, parent):
        if isinstance(literal, StringLitNode):
            if isinstance(parent, ReRangeNode) and self.skip_re_range:
                return
            literal.value = literal.value.translate(self.table)

# public API
def translate(ast, integer_flag, skip_re_range, vstringfuzzx):
    if integer_flag:
        character_set = WITH_INTEGERS
    else:
        character_set = WITHOUT_INTEGERS

    shuffler = StringShuffler(character_set)
    if vstringfuzzx:
        transformed = process_vsfx(ast, VSFX_TRANSLATE, shuffler.get_charpair())
    else:
        transformed = TranslateTransformer(ast, shuffler, skip_re_range).walk()
        
    return transformed
