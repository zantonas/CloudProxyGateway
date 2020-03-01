from cloudproxygateway.provider.s3_provider import S3Provider, S3CompatibleProvider
from cloudproxygateway.gateway.redis_gateway import RedisGateway
from cloudproxygateway.constants import PROVIDER_S3

import json


def get_gateway_conf():
    """
    Returns the gateway config.
    """
    with open('conf/gateway.json') as f:
        return json.load(f)


def get_authenticated_user():
    """
    Temporary Function until Active Directory integration
    has been developed
    """
    return "zantonas"


def get_s3_region(endpoint):
    """
    Extracts the public S3 region from the endpoint.

    :param endpoint: The public S3 endpoint.
    """
    return endpoint.split('s3.', 1)[1].split('.amazonaws.com')[0]


def get_object_store_connection():
    """
    Returns a connection object of the associated provider, where the
    user request needs to be made.
    """
    try:
        access_key = get_authenticated_user()
        r = RedisGateway()
        access_key, secret_key, endpoint, provider = r.get_storage_credentials(access_key)
        if provider == PROVIDER_S3:
            region = get_s3_region(endpoint)
            return S3Provider(access_key, secret_key, region).get_connection()
        else:
            return S3CompatibleProvider(access_key, secret_key, endpoint).get_connection()
    except Exception as ex:
        raise Exception(ex)


def load_swagger(app):
    """
    Loads the swagger ui.
    """
    from flask_swagger_ui import get_swaggerui_blueprint
    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'
    SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Cloud Proxy Gateway"
        }
    )
    app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
