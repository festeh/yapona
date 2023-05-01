from yapona.state import IdleState, RunningState
from abc import ABC


class Hook(ABC):

    def on_start(self, state: IdleState):
        pass

    def on_interrupt(self, state: RunningState):
        pass

    def on_update(self, state: RunningState):
        pass

    def on_done(self, state: RunningState):
        pass


class HookCollection(Hook):

    def __init__(self, hooks) -> None:
        self.hooks = hooks

    def on_start(self, state: IdleState):
        for hook in self.hooks:
            hook.on_start(state)

    def on_interrupt(self, state: RunningState):
        for hook in self.hooks:
            hook.on_interrupt(state)

    def on_done(self, state: RunningState):
        for hook in self.hooks:
            hook.on_done(state)

    def on_update(self, state: RunningState):
        for hook in self.hooks:
            hook.on_update(state)
