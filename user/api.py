# -*- coding:utf-8 -*-
from django.core.cache import cache

from common import errors
from lib.http import render_json
from lib.sms import send_verify_code
from lib.sms import check_vcode
from user.forms import ProfileForm
from user.logic import save_upload_file
from user.logic import upload_avatar_to_qiniu
from user.models import User


def get_verify_code(request):
    phonenum = request.GET.get('phonenum')
    send_verify_code(phonenum)
    return render_json(None)

def login(request):
    phonenum = request.POST.get('phonenum')
    vcode = int(request.POST.get('vcode'))
    if check_vcode(phonenum, vcode):
        user = User.objects.get_or_create(phonenum=phonenum)
        request.session['uid'] = user.id
        return render_json(user.to_dict())
    else:
        return render_json(None, errors.VcodeError.code)


def show_profile(request):
    '''查看个人资料'''
    user = request.user

    key = f'Profile-{user.id}'
    result = cache.get(key)
    if result is None:
        result = user.profile.to_dict()
        cache.set(key, result)

    return render_json(result)


def modify_profile(request):
    '''修改个人资料'''
    form = ProfileForm(request.POST)
    if form.is_valid():
        profile = form.save(commit=False)
        profile.id = request.user.id
        profile.save()
        result = profile.to_dict
        return render_json(result)
    else:
        return render_json(form.errors, errors.ProfileError.code)


def upload_avatar(request):
    '''上传个人形象'''
    avatar = request.FILES.get('avatar')
    filepath,filename = save_upload_file(request.user, avatar)
    upload_avatar_to_qiniu(request.user, filepath, filename)
    return render_json(None)