from abc import abstractmethod

from ntcore import Publisher, NetworkTableInstance


class Loggable:
    def __init__(self):
        self._pubs: dict[str, Publisher] = dict()
        self._inst = NetworkTableInstance.getDefault()

    def getSubtable(self) -> str:
        return "/SmartDashboard"

    def log(self, name: str, value):
        pub = self._pubs.get(name, None)

        if not pub:
            if isinstance(value, float):


        pub.publish(value)


    def createVariable(self, initial, name=None):
        if not name:
            # TODO Lookup variable name
            pass

class




