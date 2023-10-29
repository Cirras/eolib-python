from abc import ABC, abstractproperty


class Type(ABC):
    @abstractproperty
    def name(self):
        pass

    @abstractproperty
    def fixed_size(self):
        pass

    @abstractproperty
    def bounded(self):
        pass
