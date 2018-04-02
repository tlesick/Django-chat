# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
import json
from apps.User.models import *


def homepage(request):
    user = User.objects.get(id = request.session['user_id'])
    return render(request, 'chat/index.html', {'user': user})


def room(request, room_name):
    user = User.objects.get(id = request.session['user_id'])
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)), 'user':user})


        
