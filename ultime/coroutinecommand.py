import inspect
from typing import Optional, Generator

import commands2


class CoroutineCommand(commands2.Command):
    def __init__(self):
        super().__init__()
        self.__gen: Optional[Generator] = None
        self.__is_gen_finished = False

        if not inspect.isgeneratorfunction(self.coroutine):
            raise TypeError(
                f"The coroutine function of command '{self.__class__.__name__}' does not contain 'yield' statements."
            )

    def coroutine(self):
        raise NotImplementedError(
            f"The coroutine of command '{self.__class__.__name__}' is not implemented"
        )

    def initialize(self):
        if self.__gen:
            self.__gen.close()

        self.__is_gen_finished = False
        self.__gen = self.coroutine()

    def execute(self):
        try:
            if not self.__is_gen_finished:
                next(self.__gen)
        except StopIteration:
            self.__is_gen_finished = True

    def isFinished(self) -> bool:
        return self.isCoroutineFinished()

    def isCoroutineFinished(self) -> bool:
        return self.__is_gen_finished
