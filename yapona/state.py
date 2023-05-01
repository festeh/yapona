from abc import ABC, abstractmethod
import time
from yapona.utils import generate_id


class State(ABC):

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def is_done(self):
        pass


class IdleState(State):

    def __init__(self):
        self.id = generate_id()

    def update(self):
        pass

    def is_done(self):
        return False


class RunningState(State):

    def __init__(self, state_id, duration=60 * 20):
        self.id = state_id
        self.start_time = time.time()
        self.cur_time = self.start_time
        self.duration = duration
        self.delta = self.cur_time - self.start_time

    def update(self):
        self.cur_time = time.time()
        self.delta = (self.cur_time - self.start_time)

    def is_done(self):
        return self.delta >= self.duration
