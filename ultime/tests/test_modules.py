from ultime.module import Module, ModuleList


class ModuleA(Module):
    def __init__(self):
        super().__init__()
        self.called_robot_periodic = 0
        self.called_autonomous_init = 0

    def robotPeriodic(self) -> None:
        self.called_robot_periodic += 1

    def autonomousInit(self) -> None:
        self.called_autonomous_init += 1

    def initSendable(self, builder):
        pass


class ModuleB(Module):
    def __init__(self):
        super().__init__()
        self.called_robot_periodic = 0
        self.called_autonomous_exit = 0

    def robotPeriodic(self) -> None:
        self.called_robot_periodic += 1

    def autonomousExit(self) -> None:
        self.called_autonomous_exit += 1


class ModuleBChild(ModuleB):
    pass


def test_module_list():
    module_a = ModuleA()
    module_b = ModuleB()

    modules = ModuleList(module_a)
    modules.addModules(module_b)

    modules.robotPeriodic()
    modules.autonomousInit()
    modules.autonomousExit()
    modules.robotPeriodic()

    assert module_a.called_robot_periodic == 2
    assert module_a.called_autonomous_init == 1
    assert module_b.called_robot_periodic == 2
    assert module_b.called_autonomous_exit == 1


def test_redefines_init_sendable():
    module_a = ModuleA()
    module_b = ModuleB()

    modules = ModuleList(module_a)
    modules.addModules(module_b)

    assert module_a.redefines_init_sendable
    assert not module_b.redefines_init_sendable


def test_calls_parent_methods():
    module_b_child = ModuleBChild()

    modules = ModuleList(module_b_child)

    modules.robotPeriodic()

    assert module_b_child.called_robot_periodic == 1
