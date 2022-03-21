import csv
from ast import literal_eval

file = open('./reference/mapping.csv', mode='r', encoding='utf-8-sig')
reader = csv.reader(file)
header = next(reader)
rows = [[int(y) for y in x] for x in reader]
file.close()

conversion_dicts = {
    'exon': {x[0]: dict(zip(header, x)) for x in rows},
    'nc_000023.11': {range(x[2], x[1]): dict(zip(header, x)) for x in rows},
    'nc_000023.10': {range(x[4], x[3]): dict(zip(header, x)) for x in rows},
    'nm_004006.2': {range(x[5], x[6]): dict(zip(header, x)) for x in rows}
}


def convert(num, ref='nm_004006.2'):
    if ref == 'exon':
        left = convert(conversion_dicts['exon'].get(num, {}).get('cds_start'),
                       ref='nm_004006.2')
        right = convert(conversion_dicts['exon'].get(num, {}).get('cds_end'),
                        ref='nm_004006.2')

    for key, value in conversion_dicts[ref].items():
        if num in key:
            break

    exon = conversion_dicts[ref][key]['exon']

    if ref in ['nc_000023.10', 'nc_000023.11']:
        diff = max(key) - num + 1
    else:
        diff = num - min(key)

    hg38 = conversion_dicts[ref][key]['start_hg38'] - diff
    hg19 = conversion_dicts[ref][key]['start_hg19'] - diff
    cds = conversion_dicts[ref][key]['start_cds'] + diff

    res = {
        'nm_004006.2': cds,
        'exon': exon,
        'nc_000023.11': hg38,
        'nc_000023.10': hg19,
    }

    return res
