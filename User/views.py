from SmartDjango import Analyse
from django.views import View

from Base.auth import Auth
from User.models import UserP


class UserV(View):
    @staticmethod
    @Auth.require_login
    def get(r):
        """ GET /api/user/

        获取我的信息
        """
        user = r.user
        user.update()
        return user.d()


class SSV(View):
    @staticmethod
    @Auth.require_login
    @Analyse.r(b=[UserP.action])
    def put(r):

        """ PUT /api/user/ss

        修改VPN信息
        """

        action = r.d.action
        user = r.user
        actions = dict(
            on=user.do_ss_on,
            off=user.do_ss_off,
            reset=user.do_ss_reset,
        )
        actions[action]()

        return user.d()
