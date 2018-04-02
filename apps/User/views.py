# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from apps.User.models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

def index(request):
    try:
        user = User.objects.get(id = request.session['user_id'])
        if len(user) > 0:
            return redirect('/chat/homepage')
        else:
            session.clear()
            return render(request, 'user/index.html')
    except:
        return render(request, 'user/index.html')

def registration(request):
    return render(request, 'user/registration.html')

def register(request):
    new_user = User.objects.register(request.POST)
    if 'error_msg' in new_user:
        for e in new_user['error_msg']:
            messages.error(request, e)
        return redirect('/user/registration')
    else:
        for i in new_user['success']:
            messages.success(request, i)
        try:
            session.clear()
        except:
            pass
        password = request.POST['password']
        request.session['user_id'] = new_user['new_user'].id
        return redirect('/chat/homepage')
 

def login_process(request):
    print ('check')
    logged_user = User.objects.login(request.POST)
    print ('breaks in models prob')
    if 'error_msg' in logged_user:
        for e in logged_user['error_msg']:
            messages.error(request, e)
        return redirect('/')
    else:
        request.session.clear()
        request.session['user_id'] = logged_user['logged_user'].id
        return redirect('/chat/homepage')





# def update(request):
#     user = User.objects.get(id = request.session['user_id'])
#     update_user = User.objects.edit(request.POST, user.id)
#     if 'error_messages' in update_user:
#         for e in update_user['error_messages']:
#             messages.error(request, e)
#         return redirect('/user/edit')
#     else:
#         for i in update_user['success']:
#             messages.success(request, i)
#         return redirect('/chat/homepage')

# def show(request, id):
#     show_user = User.objects.get(id = id)
#     content = {
#         'user': show_user,
#     }
#     return render(request, 'user/show.html', content)


def logout(request):
    request.session.clear()
    return redirect("/")