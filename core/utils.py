from core.provider.s3_provider import S3Provider, S3CompatibleProvider
from core.gateway.redis_gateway import RedisGateway
from core.constants import PROVIDER_S3

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


def get_swagger_json():
    """
    Returns the swagger doc.
    """
    return json.dumps({
        "swagger": "2.0",
        "info": {
            "title": "Cloud Proxy",
            "version": "0.1"
        },
        "consumes": [
            "application/json"
        ],
        "produces": [
            "application/json"
        ],
        "paths": {
            "/buckets/": {
                "parameters": [
                ],
                "get": {
                    "operationId": "list_buckets",
                    "summary": "List buckets",
                    "description": "Lists all buckets associated to the user.\n",
                    "produces": [
                        "application/json"
                    ],
                    "responses": {
                        "200": {
                            "description": "200 response",
                            "examples": {
                                "application/json": "{'response':[{'CreationDate':'Thu, 27 Feb 2020 00:02:08 GMT','Name':'my-bucket-01'},{'CreationDate':'Thu, 27 Feb 2020 00:26:53 GMT','Name':'my-bucket-02'},{'CreationDate':'Wed, 26 Feb 2020 23:50:44 GMT','Name':'zach-bucket-03'}]}"
                            }
                        }
                    }
                }
            }
        }
    })
