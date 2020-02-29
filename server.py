from flask import Flask, redirect, abort
from core.utils import get_object_store_connection, load_swagger
from core.constants import HTTP_GET, HTTP_PUT, HTTP_POST, HTTP_DELETE

app = Flask(__name__)


@app.route('/buckets/', methods=[HTTP_GET])
def metadata_buckets_from_cloud():
    """
    Returns the metadata content of all buckets.
    """
    conn = get_object_store_connection()
    buckets = conn.list_buckets()
    response = {'response': buckets['Buckets']}
    return response


@app.route('/objects/<string:bucket>/', methods=[HTTP_GET])
def metadata_objects_from_cloud(bucket):
    """
    Returns the metadata content of all objects associated with
    the bucket.

    :param bucket: The requested bucket
    """
    conn = get_object_store_connection()
    try:
        objects = [obj for obj in conn.list_objects_v2(Bucket=bucket)['Contents']]
        response = {'response': objects}
        return response
    except Exception:
        abort(404)


@app.route('/objects/<string:bucket>/<string:obj>', methods=[HTTP_GET])
def redirect_presigned_get_to_cloud(bucket, obj):
    """
    Returns a pre-signed url which can be used to download the
    the data of the requested object.

    :param bucket: The requested bucket
    :param obj: The requested object
    """
    conn = get_object_store_connection()
    url = conn.generate_presigned_url(
        ClientMethod='get_object',
        Params={'Bucket': bucket, 'Key': obj},
        ExpiresIn=3600,
    )
    response = redirect(url, code=302)
    return response


@app.route('/objects/<string:bucket>/<string:obj>', methods=[HTTP_PUT, HTTP_POST])
def redirect_presigned_post_to_cloud(bucket, obj):
    """
    Returns a pre-signed url which can be used to upload data
    to the requested object.

    :param bucket: The requested bucket
    :param obj: The requested object
    """
    conn = get_object_store_connection()
    url = conn.generate_presigned_post(
        Bucket=bucket, Key=obj, ExpiresIn=3600)
    return url


@app.route('/objects/<string:bucket>/<string:obj>', methods=[HTTP_DELETE])
def delete_object_from_cloud(bucket, obj):
    """
    Deletes a requested object.

    :param bucket: The requested bucket
    :param obj: The requested object
    """
    conn = get_object_store_connection()
    try:
        response = conn.delete_object(Bucket=bucket, Key=obj)
        return response
    except Exception:
        abort(404)


if __name__ == '__main__':
    load_swagger(app)
    app.run(host='127.0.0.1', port=5000)
