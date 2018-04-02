# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from apps.User import models as User_models
from django.db import models

class Messages(models.Model):
    messages = models.CharField(max_length=255)
    user_sender = models.ForeignKey(User_models.User, on_delete=models.CASCADE, related_name="user_sender")
    user_receiver = models.ManyToManyField(User_models.User, related_name="user_receiever")
