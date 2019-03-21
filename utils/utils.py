import os
from django.utils.datetime_safe import datetime


def upload_to(instance, filename):
    date = datetime.now()
    filename, extension = filename.rsplit(".", 1)
    filename = "%d-%d-%d-%d-%d-%d-%d.%s" % (date.year, date.month, date.day, date.hour,
                                            date.minute, date.second, date.microsecond, extension)
    if extension.lower() == "pdf":
        filename = os.path.join('pdf', filename)
    else:
        filename = os.path.join('avatars', filename)
    return filename
