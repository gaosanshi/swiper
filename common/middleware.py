import logging
from django.utils.deprecation import MiddlewareMixin

from common import errors
from lib.http import render_json
from user.models import User


err_logger = logging.getLogger('err')


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
            return render_json(None, errors.LoginRequire.code)
        else:
            try:
                user = User.objects.get(uid)
            except User.DoesNotExist:
                return render_json(None, errors.UserNotExist.code)
            else:
                # 将user对象添加到request
                request.user = user


class LogicErrorMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        '''异常处理'''
        if isinstance(exception, errors.LogicError):
            err_logger.error(f'LogicError: {exception}')
            # 处理逻辑错误
            return render_json(None, exception.code)
        # else:
        #     # 处理程序错误
        #     error_info = format_exception(*exc_info())
        #     err_log.error(''.join(error_info))# 将异常信息输出到错误日志
        #     return render_json(None, exception.code)
