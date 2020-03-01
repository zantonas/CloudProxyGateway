import boto3

from cloudproxygateway.provider.abstract_provider import AbstractProvider


class S3Provider(AbstractProvider):
    """
    Provider to a public S3 object store.
    """
    def __init__(self, access_key, secret_key, region):
        """
        Initializes a public S3 provider.

        :param access_key: The access_key associated with the public S3 account
        :param secret_key: The secret_key associated with the public S3 account
        :param region: The region associated with the public S3 account
        """
        super().__init__(access_key, secret_key, region)

    def _login(self, access_key, secret_key, region):
        """
        Returns a public S3 connection object.

        :param access_key: The access_key associated with the public S3 account
        :param secret_key: The secret_key associated with the public S3 account
        :param region: The region associated with the public S3 account
        """
        return boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )


class S3CompatibleProvider(AbstractProvider):

    def __init__(self, access_key, secret_key, endpoint):
        """
        Initializes a private S3 provider.

        :param access_key: The access_key associated with the private S3 account
        :param secret_key: The secret_key associated with the private S3 account
        :param endpoint: The endpoint associated with the private S3 account
        """
        super().__init__(access_key, secret_key, endpoint)

    def _login(self, access_key, secret_key, endpoint):
        """
        Returns a private S3 connection object.

        :param access_key: The access_key associated with the private S3 account
        :param secret_key: The secret_key associated with the private S3 account
        :param endpoint: The endpoint associated with the private S3 account
        """
        return boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            endpoint=endpoint
        )