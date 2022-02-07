from abc import abstractmethod
from behavior_base import PSENode, EventNode


class BehaviorMat:
    code_map = {}
    fields = []  # maybe divide to event, ev_features, trial_features
    time_unit = None
    eventlist = None

    def __init__(self, animal, session):
        self.animal = animal
        self.session = session
        self.time_aligner = lambda s: s  # provides method to align timestamps

    @abstractmethod
    def todf(self):
        return NotImplemented

    def align_ts2behavior(self, timestamps):
        return self.time_aligner(timestamps)


class GoNogoBehaviorMat(BehaviorMat):
    code_map = {
        3: ('in', 'in'),
        4: ('out', 'out'),
        44: ('out', 'out'),
        81.01: ('outcome', 'no-go_correct_unrewarded'),
        81.02: ('outcome', 'go_correct_unrewarded'),
        81.12: ('outcome', 'go_correct_reward1'),
        81.22: ('outcome', 'go_correct_reward2'),
        82.02: ('outcome', 'go_incorrect'),
        83: ('outcome', 'missed'),
        84: ('outcome', 'abort'),
        9.01: ('water_valve', '1'),
        9.02: ('water_valve', '2'),
        9.03: ('water_valve', '3')
    }
    # 7.0n -> sound n on (n = 1-16)
    for i in range(1, 17):
        code_map[(700 + i) / 100] = ('sound_on', str(i))

    def __init__(self, animal, session, outfile):
        super().__init__(animal, session)

    def todf(self):
        pass
