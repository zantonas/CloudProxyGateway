from core.gateway.abstract_gateway import AbstractGateway
from core import utils

import redis


class RedisGateway(AbstractGateway):
    """
    Gateway to redis memory store.
    Stores data in the following format:
    '<authenticated_user>', '<access_key>,<secret_key>,<endpoint>,<provider_type>'
    """
    def __init__(self):
        """
        Initialize the RedisGateway.
        """
        conf = utils.get_gateway_conf()
        self.r = redis.Redis(host=conf['host'], port=conf['port'])

    def get_storage_credentials(self, authenticated_user):
        """
        Retrieves the value from redis using the authenticated_user key.

        :param authenticated_user: The authenticated_user.
        :return: <access_key>, <secret_key>, <endpoint>, <provider_type>
        """
        try:
            credentials = self.r.get(authenticated_user).decode('utf-8').split(',', 3)
            return credentials[0], credentials[1], credentials[2], credentials[3]
        except Exception:
            raise Exception('Key not found')
