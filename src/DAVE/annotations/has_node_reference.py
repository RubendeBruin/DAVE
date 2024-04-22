from abc import abstractmethod
class HasNodeReference:

    @abstractmethod
    def update(self):
        pass
    @property
    @abstractmethod
    def is_valid(self):
        pass