from django.utils.deprecation import MiddlewareMixin

from common import errors
from lib.http import render_json
from user.models import User


class AuthMiddleware(MiddlewareMixin):
    white_list = [
        '/api/user/vcode',
        '/api/user/login',
    ]

    def process_request(self, request):
        if request.path in self.white_list:
            return
        uid = request.session.get('uid')
        if uid is None:
            return render_json(None, errors.LOGIN_REQUIRE)
        else:
            try:
                user = User.objects.get(uid)
            except User.DoesNotExist:
                return render_json(None, errors.USER_NOT_EXIST)
            else:
                # 将user对象添加到request
                request.user = user
