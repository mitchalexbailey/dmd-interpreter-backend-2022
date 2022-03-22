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
    digits = re.findall(r'[+-]*\d+', inp)
    if len(digits) == 0:
        return []

    nums = [int(x) for x in digits if '-' not in x and '+' not in x]
    introns = [int(x) for x in digits if '-' in x or '+' in x]
    if len(introns)==0:
        introns = [0 for x in nums]

    return nums, introns


def xcgConvert(inp):
    """
    Convert numbers from user input to CDS, genomic and/or exon

    Returns dict with each set of numbers
    """
    ref = getRef(inp)
    nums, introns = getNums(inp)
    print(introns)

    dicts = []
    for x in list(zip(nums, introns)):
        dicts += [convert(x[0], intron=x[1], ref=ref)]

    res = {x: [] for x in dicts[0].keys()}
    for d in dicts:
        for x, y in d.items():
            res[x] += [y]

    return res
