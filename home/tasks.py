from bucket import Bucket
from celery import shared_task

bucket = Bucket()


def all_bucket_objects_task():
    return bucket.get_objects()


@shared_task
def delete_object_task(key):
    bucket.delete_object(key)
    return None


@shared_task
def download_object_task(key):
    bucket.download_object(key)
    return None
