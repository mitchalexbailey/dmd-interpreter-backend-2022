import csv
from ast import literal_eval

file = open('./reference/mapping.csv', mode='r', encoding='utf-8-sig')
reader = csv.reader(file)
header = next(reader)
rows = [[int(y) for y in x] for x in reader]
file.close()

conversion_dicts = {
    'exon': {x[0]: dict(zip(header, x)) for x in rows},
    'nc_000023.11': {range(x[2], x[1]+1): dict(zip(header, x)) for x in rows},
    'nc_000023.10': {range(x[4], x[3]+1): dict(zip(header, x)) for x in rows},
    'nm_004006.2': {range(x[5], x[6]+1): dict(zip(header, x)) for x in rows}
}


def get_closest(num):
    flat_lst = []
    for x in list(conversion_dicts['nc_000023.11']):
        if type(x) == list:
            flat_lst += [y for y in x]
        elif type(x) == range:
            flat_lst += [min(x), max(x)]
        else:
            flat_lst += [x]

    diffs = [x-num for x in flat_lst]
    abss = [abs(x) for x in diffs]
    min_abs = min(abss)
    ind = abss.index(min_abs)
    intron = diffs[ind]
    num = flat_lst[ind]
    key = list(conversion_dicts['nc_000023.11'])[int(ind/2)]

    return num, intron, key


def convert(num, intron, ref):
    if ref == 'exon':
        left = convert(conversion_dicts['exon'].get(num, {}).get('cds_start'),
                       ref='nm_004006.2')
        right = convert(conversion_dicts['exon'].get(num, {}).get('cds_end'),
                        ref='nm_004006.2')

    found = False
    for key, value in conversion_dicts[ref].items():
        if num in key:
            found = True
            break

    if not found:
        num, intron, key = get_closest(num)

    exon = conversion_dicts[ref][key]['exon']

    if ref in ['nc_000023.10', 'nc_000023.11']:
        diff = max(key) - num
    else:
        diff = num - min(key)

    hg38 = conversion_dicts[ref][key]['start_hg38'] - diff - intron
    hg19 = conversion_dicts[ref][key]['start_hg19'] - diff - intron
    cds = conversion_dicts[ref][key]['start_cds'] + diff

    res = {
        'nm_004006.2': cds,
        'intron': intron,
        'exon': exon,
        'nc_000023.11': hg38,
        'nc_000023.10': hg19,
    }

    return res
