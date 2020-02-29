import os
import requests


def list_buckets():
    """
    List all buckets.
    """
    r = requests.get('http://127.0.0.1:5000/buckets/')
    print(r)
    print(r.text)


def list_objects(bucket='my_bucket'):
    """
    List all objects associated with a bucket.

    :param bucket: The requested bucket
    """
    r = requests.get(f'http://127.0.0.1:5000/objects/{bucket}')
    print(r)
    print(r.text)


def download_object(bucket='my_bucket', obj='my_object'):
    """
    Download an object.

    :param bucket: The requested bucket
    :param obj: The requested object
    """
    r = requests.get(f'http://127.0.0.1:5000/objects/{bucket}/{obj}')
    print(r)
    print(r.text)


def upload_object(bucket='my_bucket', file_path='full_path_to_file'):
    """
    Uploads an object.

    :param bucket: The requested bucket
    :param file_path: The full path to the file.
    """
    obj_name = os.path.basename(file_path)
    with open(file_path, 'rb') as f:
        files = {'file': (obj_name, f)}
        r = requests.post(f'http://127.0.0.1:5000/objects/{bucket}/{obj_name}')
        try:
            post_response = requests.post(
                r.json()['url'], data=r.json()['fields'], files=files)
            print(post_response)
            print(post_response.text)
        except Exception as ex:
            raise Exception(f'Unable to post object: {ex}')


def delete_object(bucket='my_bucket', obj='my_object'):
    """
    Deletes an object.

    :param bucket: The requested bucket
    :param obj: The requested object
    """
    r = requests.delete(f'http://127.0.0.1:5000/objects/{bucket}/{obj}')
    print(r)
    print(r.text)
