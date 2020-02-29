from abc import ABC, abstractmethod


class AbstractGateway(ABC):
    """
    Gateway to an abstract data store.
    """

    @abstractmethod
    def get_storage_credentials(self, authenticated_user):
        """
        Retrieves the value from the gateway using the authenticated_user key.

        :param authenticated_user: The authenticated_user.
        """
        pass
