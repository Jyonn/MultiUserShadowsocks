from SmartDjango import Analyse
from django.views import View
from smartify import P

from Base.auth import Auth
from Base.common import qt_manager
from User.models import User


class OAuthView(View):
    @staticmethod
    @Analyse.r(q=[P('code', '齐天簿授权码')])
    def get(r):
        code = r.d.code

        body = qt_manager.get_token(code)

        token = body['token']
        qt_user_app_id = body['user_app_id']

        user = User.create(qt_user_app_id, token)

        user.update()
        return Auth.get_login_token(user)
