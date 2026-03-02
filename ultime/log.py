import inspect
import weakref
from typing import Optional, List

from ntcore import NetworkTableInstance, PubSubOptions


class Loggable:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._logvalues: dict[str, LogValue] = dict()

    def getSubtable(self) -> str:
        """
        Should always return a name ending with a slash.
        :return:
        """
        return "/SmartDashboard/"

    def log(self, name: str, value):
        logvalue = self._logvalues.get(name, None)

        if not logvalue:
            logvalue = LogValue(self.getSubtable() + name, value)
            self._logvalues[name] = logvalue

        logvalue.set(value)

    def logConstant(self, name: str, value):
        value = LogValue(self.getSubtable() + name, value)
        value.close()

    def logValues(self):
        """
        Override to log custom values.
        """
        pass

    def flush(self):
        self.logValues()
        for value in self._logvalues.values():
            value.flush()

    def createProperty(self, initial_value, subscribe=False, name=None):
        if not name:
            curframe = inspect.currentframe()
            calframes = inspect.getouterframes(curframe, 1)
            calframe = calframes[1]
            code_line = calframe.code_context[0]
            name = code_line.split("=")[0].strip()[5:]

        log_value = LogValue(self.getSubtable() + name, initial_value, subscribe)
        self._logvalues[name] = log_value
        setattr(type(self), name, LogProperty(name))

        return initial_value


class LogValue[T]:
    def __init__(
        self,
        key: str,
        initial_value: T,
        subscribe=False,
        inst: NetworkTableInstance = None,
    ):
        self._key = key
        self._value = initial_value
        self._type = type(initial_value)

        if not inst:
            inst = NetworkTableInstance.getDefault()

        get_topic = {
            int: inst.getIntegerTopic,
            float: inst.getFloatTopic,
            str: inst.getStringTopic,
            bool: inst.getBooleanTopic,
            list: inst.getDoubleArrayTopic,
        }.get(self._type, None)

        if not get_topic:
            raise TypeError(f"Type '{self._type}' is not supported: {initial_value}")

        self._topic = get_topic(self._key)
        self._pub = self._topic.publish()
        self._pub.set(self._value)
        self._has_changed = False

        self._sub = None
        if subscribe:
            self._sub = self._topic.subscribe(
                self._value, PubSubOptions(pollStorage=1, disableLocal=True)
            )

    def flush(self):
        if self._has_changed:
            self._pub.set(self._value)
            self._has_changed = False
        elif self._sub:
            changes = self._sub.readQueue()
            if changes:
                self._value = changes[-1].value

    def set(self, value: T):
        if value != self._value:
            self._has_changed = True
            self._value = value

    def get(self) -> T:
        return self._value

    def close(self):
        self._pub.close()
        if self._sub:
            self._sub.close()


class LogProperty:
    def __init__(self, name: str):
        self._name = name

    def __get__(self, obj: Loggable, objtype=None):
        log_value = obj._logvalues[self._name]
        return log_value.get()

    def __set__(self, obj: Loggable, value):
        obj._logvalues[self._name].set(value)


class Logger(Loggable):
    _instance: Optional[Logger] = None

    @staticmethod
    def getInstance() -> Logger:
        return Logger()

    def __new__(cls) -> Logger:
        if cls._instance is None:
            inst = super().__new__(cls)
            inst._loggables = weakref.WeakSet()
            cls._instance = inst
            return inst
        return cls._instance

    def __init__(self):
        super().__init__()
        # Ne pas mettre d'attribut ici, mais les mettre dans le __new__.

    def addLoggable(self, loggable: Loggable):
        self._loggables.add(loggable)

    def logValues(self):
        for loggable in self._loggables:
            loggable.flush()

    def flush(self):
        super().flush()
        NetworkTableInstance.getDefault().flushLocal()

    def getSubsystem(self):
        return "/"
