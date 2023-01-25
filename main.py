class Variant:

    def __init__(self, user_input):
        from interpreter_functions_api import getInput, exInput, getType, xcgConvert
        self.user_input = user_input
        self.interpreted_input = getInput(user_input)
        self.ex_input = exInput(user_input)
        self.nums = xcgConvert(user_input)
        self.type = getType(user_input)

        self._in_frame()
        self._exon_skip()

    def _in_frame(self):
        nums = self.nums.get('nm_004006.2')
        mut_length = max(nums) - min(nums)
        if mut_length % 3 + 1 == 0 or mut_length == 0:
            self.frame_shift = False
        else:
            self.frame_shift = True

    def _exon_skip(self):
        from interpreter_functions_api import xcgConvert

        if self.type not in ['deletion', 'duplication'] or not self.frame_shift or False in self.nums.get('exon_border'):
            self.exon_skip = None

        nums = self.nums.get('nm_004006.2')
        mut_length = max(nums)-min(nums)+1

        exons = self.nums.get('exon')
        potential_skips = {}
        for ex in (min(exons)-1, max(exons)+1):
            ex_nums = xcgConvert(f'del ex {ex}')
            potential_skips[ex] = max(ex_nums.get('nm_004006.2'))-min(ex_nums.get('nm_004006.2'))+1

        skips = [x for x, y in potential_skips.items() if (mut_length + y) % 3 == 0]
        if (mut_length + sum(potential_skips.values())) % 3 == 0:
            skips += [tuple(potential_skips.keys())]

        self.exon_skip = skips
