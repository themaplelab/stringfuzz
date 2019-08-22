import subprocess
import os
import typing as ty

from stringfuzz.generator import generate
from stringfuzz.constants import SMT_25_STRING
from stringfuzz.parser import parse

VSFX_TRANSLATE = "translate"
VSFX_REVERSE = "reverse"
VSFX_MULTIPLY = "multiply"


def process_vsfx(problem: list, mode: str,
    param: ty.List[ty.Union[str, int]]=None,
    args: ty.Union[None, ty.List]=None) -> list:
    if args is None:
        args = []
    if param is None:
        param = []

    vsfx_path = os.path.join(os.environ["VSFX_PATH"], "vsfx")

    proc = subprocess.run(
        [vsfx_path, mode] + param + args,
        stdout=subprocess.PIPE,
        input=generate(problem, SMT_25_STRING),
        universal_newlines=True
    )

    proc.check_returncode()
    return parse(proc.stdout, SMT_25_STRING)