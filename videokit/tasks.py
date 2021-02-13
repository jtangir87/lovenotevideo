from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.core.files import File
from django.core.files.storage import default_storage

import os
import subprocess
from pathlib import Path
import requests
import boto3

from celery import shared_task

from videokit.apps import VideokitConfig


@shared_task
def generate_video(file_name, source_file_name, options=[]):
    base = getattr(settings, "BASE_DIR", "")
    media_root = getattr(settings, "MEDIA_ROOT", "")

    original_file_root = getattr(settings, "ORIGINAL_ROOT", "")

    source_file = os.path.join(original_file_root, source_file_name)

    if not os.path.exists(source_file):
        raise IOError("%s does not exist." % source_file)

    temp_file_dir = os.path.join(
        base, getattr(settings, "VIDEOKIT_TEMP_DIR",
                      VideokitConfig.VIDEOKIT_TEMP_DIR)
    )
    temp_file = os.path.join(temp_file_dir, os.path.basename(file_name))

    if not os.path.exists(temp_file_dir):
        try:
            os.makedirs(temp_file_dir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    if not os.path.isdir(temp_file_dir):
        raise IOError("%s exists and is not a directory." % temp_file_dir)

    process = subprocess.Popen(
        ["ffmpeg", "-i", source_file, "-y"] + options + [temp_file]
    )

    process.wait()

    processed_file = file_name
    with File(open(temp_file, "rb")) as f:
        # f = File(open(temp_file, "rb"))
        default_storage.save(processed_file, f)
        f.close()

    # base = getattr(settings, "BASE_DIR", "")
    # media_root = getattr(settings, "ORIGINAL_ROOT", "")

    # aws_file_name = "{}/{}{}".format(
    #     settings.AWS_LOCATION, media_root, source_file_name
    # )

    # temp_file_dir = os.path.join(
    #     base, getattr(settings, "VIDEOKIT_TEMP_DIR",
    #                   VideokitConfig.VIDEOKIT_TEMP_DIR)
    # )

    # temp_source_file = os.path.join(
    #     media_root, os.path.basename(file_name))

    # session = boto3.session.Session()
    # client = session.client(
    #     "s3",
    #     region_name=settings.AWS_S3_REGION_NAME,
    #     endpoint_url=settings.AWS_S3_ENDPOINT_URL,
    #     aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    #     aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    # )
    # client.download_file(
    #     settings.AWS_STORAGE_BUCKET_NAME, aws_file_name, temp_source_file,
    # )
    # path = client.generate_presigned_url(
    #     ClientMethod="get_object",
    #     Params={"Bucket": settings.AWS_STORAGE_BUCKET_NAME, "Key": aws_file_name},
    # )

    # temp_file = os.path.join(temp_file_dir, os.path.basename(file_name))

    # if not os.path.exists(temp_file_dir):
    #     try:
    #         os.makedirs(temp_file_dir)
    #     except OSError as e:
    #         if e.errno != errno.EEXIST:
    #             raise

    # if not os.path.isdir(temp_file_dir):
    #     raise IOError("%s exists and is not a directory." % temp_file_dir)

    # process = subprocess.Popen(
    #     ["ffmpeg", "-i", temp_source_file, "-y"] + options + [temp_file]
    # )

    # process.wait()

    # processed_file = file_name
    # with File(open(temp_file, "rb")) as f:
    #     # f = File(open(temp_file, "rb"))
    #     default_storage.save(processed_file, f)
    #     f.close()

    thumbnail_name = "%s%s" % (os.path.basename(
        source_file_name.lower()), ".thumb.jpg")
    temp_thumbnail_file = os.path.join(temp_file_dir, thumbnail_name)

    thumbnail_process = subprocess.Popen(
        ["ffmpeg", "-i", source_file, "-frames",
            "1", "-y"] + [temp_thumbnail_file]
    )

    thumbnail_process.wait()

    processed_thumb_file = "%s%s" % (source_file_name.lower(), ".thumb.jpg")
    with File(open(temp_thumbnail_file, "rb")) as f:
        # f = File(open(temp_file, "rb"))
        default_storage.save(processed_thumb_file, f)
        f.close()

    os.remove(temp_file)
    os.remove(temp_thumbnail_file)
