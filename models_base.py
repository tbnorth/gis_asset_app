
from django.db import models


# imports used by models.py
import os
# import md5  # for photo file dupe checking
from django.db.models.signals import pre_save  # to calc md5 for photo
from django.conf import settings
