from utils.interpreter_helpers import convert

import re
from ast import literal_eval


def getInput(inp):
    return inp.lower().split(':')[-1]


def getRef(inp):
    if exInput(inp):
        return 'exon'

    if ':' not in inp:
        if 'c.' in inp:
            return 'nm_004006.2'  # assume NM_004006.2
        elif 'g.' in inp:  # assume hg38
            return 'nc_000023.11'
        else:
            return 'error'

    ref = inp.split(':')[0]
    return ref.lower()


def exInput(inp):
    """
    Get whether text input is refering to exon numbers or nucleotide positions
    """
    if 'x' in getInput(inp):
        return True

    return False


def getType(inp):
    inp = getInput(inp)
    if "del" in inp:
        if "ins" in inp:
            muttype = "deletion-insertion"
        else:
            muttype = "deletion"
    elif "ins" in inp:
        muttype = "insertion"
    elif "dup" in inp:
        muttype = "duplication"
    elif ">" in inp or "point" in inp or "trans" in inp:
        muttype = "substitution"
    elif "to" in inp and not ex_input:
        muttype = "substitution"
    else:
        muttype = "invalid"
    return muttype


def getNums(inp):
    """
    Extract number(s) from user input
    """
    inp = getInput(inp)
    digits = [int(x) for x in re.findall(r'\d+', inp)]
    if len(digits) == 0:
        return []

    return [digits[0], digits[-1]]


def xcgConvert(inp):
    """
    Convert numbers from user input to CDS, genomic and/or exon

    Returns dict with each set of numbers
    """
    # figure out if input is exon, cds or genomic reference
    ref = getRef(inp)
    nums = getNums(inp)

    dicts = []
    for x in nums:
        dicts += [convert(x, ref=ref)]

    res = {x: [] for x in dicts[0].keys()}
    for d in dicts:
        for x, y in d.items():
            res[x] += [y]

    return res
