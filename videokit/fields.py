from django.conf import settings
from django.core.files import File
from django.db.models.fields.files import FieldFile
from django.db.models.fields.files import FileDescriptor

from django.core.files.storage import default_storage
from datetime import datetime
from hashlib import md5
import os.path
import subprocess
import boto3
from botocore.client import Config
from videokit.apps import VideokitConfig
from videokit.tasks import generate_video


def get_video_dimensions(file):
    # session = boto3.session.Session()
    # client = session.client(
    #     "s3",
    #     region_name=settings.AWS_S3_REGION_NAME,
    #     endpoint_url=settings.AWS_S3_ENDPOINT_URL,
    #     aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    #     aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    #     config=Config(signature_version="s3"),
    # )
    # path_to_file = "{}/{}{}".format(settings.AWS_LOCATION, settings.MEDIA_ROOT, file)
    # path = client.generate_presigned_url(
    #     ClientMethod="get_object",
    #     Params={"Bucket": settings.AWS_STORAGE_BUCKET_NAME, "Key": path_to_file},
    # )
    # if os.path.isfile(path):
    #     try:
    #         process = subprocess.Popen(
    #             ["mediainfo", "--Inform=Video;%Width%", path],
    #             stdout=subprocess.PIPE,
    #             stderr=subprocess.PIPE,
    #             universal_newlines=True,
    #         )

    #         stdout, stderr = process.communicate()
    #         if process.wait() == 0:
    #             width = int(stdout.strip(" \t\n\r"))
    #         else:
    #             return (0, 0)

    #         process = subprocess.Popen(
    #             ["mediainfo", "--Inform=Video;%Height%", path],
    #             stdout=subprocess.PIPE,
    #             stderr=subprocess.PIPE,
    #             universal_newlines=True,
    #         )

    #         stdout, stderr = process.communicate()
    #         if process.wait() == 0:
    #             height = int(stdout.strip(" \t\n\r"))
    #         else:
    #             return (None, None)

    #         return (width, height)
    #     except OSError:
    #         pass

    return (None, None)


def get_video_rotation(file):
    # path = os.path.join(settings.MEDIA_ROOT, file.name)

    # if os.path.isfile(path):
    #     try:
    #         process = subprocess.Popen(
    #             ["mediainfo", "--Inform=Video;%Rotation%", path],
    #             stdout=subprocess.PIPE,
    #             stderr=subprocess.PIPE,
    #             universal_newlines=True,
    #         )

    #         stdout, stderr = process.communicate()
    #         if process.wait() == 0:
    #             try:
    #                 rotation = float(stdout.strip(" \t\n\r"))
    #             except ValueError:
    #                 rotation = 0.0

    #             return rotation
    #     except OSError:
    #         pass

    return 0.0


def get_video_mimetype(file):
    # path = os.path.join(settings.MEDIA_ROOT, file.name)

    # if os.path.isfile(path):
    #     try:
    #         process = subprocess.Popen(
    #             ["mediainfo", "--Inform=Video;%InternetMediaType%", path],
    #             stdout=subprocess.PIPE,
    #             stderr=subprocess.PIPE,
    #             universal_newlines=True,
    #         )

    #         stdout, stderr = process.communicate()
    #         if process.wait() == 0:
    #             mimetype = stdout.strip(" \t\n\r")
    #             if mimetype == "video/H264":
    #                 mimetype = "video/mp4"

    #             if mimetype == "":
    #                 mimetype = "video/mp4"
    #             return mimetype
    #     except OSError:
    #         pass

    return ""


def get_video_duration(file):
    # path = os.path.join(settings.MEDIA_ROOT, file.name)

    # if os.path.isfile(path):
    #     try:
    #         process = subprocess.Popen(
    #             ["mediainfo", "--Inform=Video;%Duration%", path],
    #             stdout=subprocess.PIPE,
    #             stderr=subprocess.PIPE,
    #             universal_newlines=True,
    #         )

    #         stdout, stderr = process.communicate()
    #         if process.wait() == 0:
    #             try:
    #                 duration = int(stdout.strip(" \t\n\r"))
    #             except ValueError:
    #                 duration = 0

    #             return duration
    #     except OSError:
    #         pass

    return 0


def get_video_thumbnail(file):
    # base = getattr(settings, "BASE_DIR", "")

    # session = boto3.session.Session()
    # client = session.client(
    #     "s3",
    #     region_name=settings.AWS_S3_REGION_NAME,
    #     endpoint_url=settings.AWS_S3_ENDPOINT_URL,
    #     aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    #     aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    #     config=Config(signature_version="s3"),
    # )
    # path_to_file = "{}/{}{}".format(settings.AWS_LOCATION, settings.MEDIA_ROOT, file)
    # path = client.generate_presigned_url(
    #     ClientMethod="get_object",
    #     Params={"Bucket": settings.AWS_STORAGE_BUCKET_NAME, "Key": path_to_file},
    # )

    # print(path)
    # path = os.path.join(settings.MEDIA_ROOT, file.name)
    thumbnail_name = "%s%s" % (file, ".thumb.jpg")
    # print(thumbnail_name)

    # temp_file_dir = os.path.join(
    #     base, getattr(settings, "VIDEOKIT_TEMP_DIR", VideokitConfig.VIDEOKIT_TEMP_DIR)
    # )
    # temp_file = os.path.join(temp_file_dir, thumbnail_name)
    # try:
    #     print("trying process")
    #     process = subprocess.Popen(
    #         ["ffmpeg", "-i", path, "-frames", "1", "-y", temp_file],
    #         stdout=subprocess.PIPE,
    #         stderr=subprocess.PIPE,
    #     )

    #     process.wait()
    #     print("waiting")
    #     with File(open(temp_file, "rb")) as f:
    #         print("open file")
    #         # f = File(open(temp_file, "rb"))
    #         default_storage.save(thumbnail_name, f)
    #         f.close()

    #     os.remove(temp_file)

    # except OSError:
    #     pass

    return thumbnail_name


class VideoFile(File):
    def _get_width(self):
        return self._get_video_dimensions()[0]

    width = property(_get_width)

    def _get_height(self):
        return self._get_video_dimensions()[1]

    height = property(_get_height)

    def _get_rotation(self):
        return self._get_video_rotation()

    rotation = property(_get_rotation)

    def _get_mimetype(self):
        return self._get_video_mimetype()

    mimetype = property(_get_mimetype)

    def _get_duration(self):
        return self._get_video_duration()

    duration = property(_get_duration)

    def _get_thumbnail(self):
        return self._get_video_thumbnail()

    thumbnail = property(_get_thumbnail)

    def _get_video_dimensions(self):
        if not hasattr(self, "_dimensions_cache"):
            self._dimensions_cache = get_video_dimensions(self)

        return self._dimensions_cache

    def _get_video_rotation(self):
        if not hasattr(self, "_rotation_cache"):
            self._rotation_cache = get_video_rotation(self)

        return self._rotation_cache

    def _get_video_mimetype(self):
        if not hasattr(self, "_mimetype_cache"):
            self._mimetype_cache = get_video_mimetype(self)

        return self._mimetype_cache

    def _get_video_duration(self):
        if not hasattr(self, "_duration_cache"):
            self._duration_cache = get_video_duration(self)

        return self._duration_cache

    def _get_video_thumbnail(self):
        if not hasattr(self, "_thumbnail_cache"):
            self._thumbnail_cache = get_video_thumbnail(self)

        return self._thumbnail_cache


class VideoFileDescriptor(FileDescriptor):
    def __set__(self, instance, value):
        previous_file = instance.__dict__.get(self.field.name)
        super(VideoFileDescriptor, self).__set__(instance, value)

        if previous_file is not None:
            self.field.update_dimension_fields(instance, force=True)
            self.field.update_rotation_field(instance, force=True)
            self.field.update_mimetype_field(instance, force=True)
            self.field.update_duration_field(instance, force=True)
            self.field.update_thumbnail_field(instance, force=True)


class VideoFieldFile(VideoFile, FieldFile):
    def delete(self, save=True):
        if hasattr(self, "_dimensions_cache"):
            del self._dimensions_cache

        if hasattr(self, "_rotation_cache"):
            del self._rotation_cache

        if hasattr(self, "_mimetype_cache"):
            del self._mimetype_cache

        if hasattr(self, "_duration_cache"):
            del self._duration_cache

        if hasattr(self, "_thumbnail_cache"):
            del self._thumbnail_cache

        super(VideoFieldFile, self).delete(save)


class VideoSpecFieldFile(VideoFieldFile):
    def _require_file(self):
        if not self.source_file:
            raise ValueError(
                "The '%s' attribute's source has no file associated with it."
                % self.field_name
            )
        else:
            self.validate()

    def delete(self, save=True):
        if hasattr(self, "_generated_cache"):
            del self._generated_cache

        super(VideoSpecFieldFile, self).delete(save)

    def validate(self):
        return self.field.video_cache_backend.validate(self)

    def invalidate(self):
        return self.field.video_cache_backend.invalidate(self)

    def clear(self):
        return self.field.video_cache_backend.clear(self)

    def generate(self):
        if not self.generating() and not self.generated():
            file_name = self.generate_file_name()

            options = []
            if self.field.format == "mp4":
                options = [
                    "-c:v",
                    "libx264",
                    "-c:a",
                    "aac",
                    "-b:v",
                    "1M",
                    "-b:a",
                    "128k",
                ]
            elif self.field.format == "ogg":
                options = [
                    "-c:v",
                    "libtheora",
                    "-c:a",
                    "libvorbis",
                    "-q:v",
                    "10",
                    "-q:a",
                    "6",
                ]
            elif self.field.format == "webm":
                options = [
                    "-c:v",
                    "libvpx",
                    "-c:a",
                    "libvorbis",
                    "-crf",
                    "10",
                    "-b:v",
                    "1M",
                ]

            self.name = file_name
            self.instance.save()

            generate_video.delay(file_name, self.source_file.name, options=options)

    def generating(self):
        if self.name:
            base = getattr(settings, "BASE_DIR", "")
            temp_file_dir = os.path.join(
                base,
                getattr(
                    settings, "VIDEOKIT_TEMP_DIR", VideokitConfig.VIDEOKIT_TEMP_DIR
                ),
            )
            temp_file = os.path.join(temp_file_dir, os.path.basename(self.name))

            if os.path.exists(temp_file):
                return True

        return False

    def generate_file_name(self):
        cachefile_dir = getattr(
            settings, "VIDEOKIT_CACHEFILE_DIR", VideokitConfig.VIDEOKIT_CACHEFILE_DIR
        )
        dir = os.path.join(cachefile_dir, os.path.split(self.source_file.name)[0])
        hash = md5()
        hash.update(
            (
                "%s%s%s"
                % (self.source_file.name, self.field.format, str(datetime.now()))
            ).encode("utf-8")
        )
        final_hash = hash.hexdigest()
        file_name = final_hash + "." + self.field.format

        return os.path.join(dir, file_name)

    def generated(self):
        if hasattr(self, "_generated_cache"):
            return self._generated_cache
        else:
            if self.name:
                if self.storage.exists(self.name):
                    self._generated_cache = True
                    return True

        return False

    @property
    def source_file(self):
        source_field_name = getattr(self.field, "source", None)
        if source_field_name:
            return getattr(self.instance, source_field_name)
        else:
            return None


class VideoSpecFileDescriptor(VideoFileDescriptor):
    pass
