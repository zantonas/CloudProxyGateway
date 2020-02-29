from abc import ABC, abstractmethod


class AbstractProvider(ABC):
    """
    Provider to an abstract object store.
    """
    @abstractmethod
    def __init__(self, *args):
        """
        Initializes an abstract provider.

        :param args: The arguments required to login to the object store
        """
        self.conn = self._login(*args)

    @abstractmethod
    def _login(self, *args):
        """
        Abstract login to the object store.

        :param args: The arguments required to login to the object store
        """
        pass

    def get_connection(self):
        """
        Returns an abstract connection object for the object store.

        :return: The connection object of the object store.
        """
        return self.conn
