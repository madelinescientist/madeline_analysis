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
    def __init__(self, animal, session, outfile):
        super().__init__(animal, session)

    def todf(self):
        pass
