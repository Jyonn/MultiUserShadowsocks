""" Adel Liu 180221

用户类
"""
import random

from django.db import models
from django.utils.crypto import get_random_string

from Base.common import deprint
from Base.dealer import Dealer
from Base.decorator import field_validator
from Base.error import Error
from Base.response import Ret


class User(models.Model):
    """
    用户类
    根超级用户id=1
    """
    ROOT_ID = 1
    L = {
        'qt_user_app_id': 16,
        'qtb_token': 256,
        'ss_pwd': 32,
        'nickname': 10,
        'avatar': 1024,
        'description': 20,
    }
    SS_CHANGE_INTERVAL = 300

    avatar = models.CharField(
        default=None,
        null=True,
        blank=True,
        max_length=L['avatar'],
    )
    nickname = models.CharField(
        max_length=L['nickname'],
        default=None,
        blank=True,
        null=True,
    )
    qt_user_app_id = models.CharField(
        default=None,
        max_length=L['qt_user_app_id'],
    )
    qtb_token = models.CharField(
        default=None,
        max_length=L['qtb_token'],
    )
    description = models.CharField(
        max_length=L['description'],
        default=None,
        blank=True,
        null=True,
    )
    port = models.PositiveSmallIntegerField(
        verbose_name='SS端口',
        default=0,
        unique=True,
    )
    ss_pwd = models.CharField(
        verbose_name='SS密码',
        default=None,
        max_length=L['ss_pwd'],
    )
    ss_on = models.BooleanField(
        verbose_name='ss状态, 0 off, 1 on',
        default=False,
    )
    ss_change_time = models.FloatField(
        null=True,
        blank=True,
        default=0,
    )
    FIELD_LIST = ['port', 'ss_pwd', 'avatar', 'nickname', 'qt_user_app_id', 'description']

    @classmethod
    def get_unique_port(cls):
        while True:
            port = random.randint(60000, 65500)
            ret = cls.get_user_by_port(port)
            if ret.error == Error.NOT_FOUND_USER:
                return port
            deprint('generate port: %s, conflict.' % port)

    @classmethod
    def _validate(cls, dict_):
        """验证传入参数是否合法"""
        return field_validator(dict_, cls)

    @staticmethod
    def get_user_by_qt_user_app_id(qt_user_app_id):
        """根据齐天用户-应用ID获取用户对象"""
        try:
            o_user = User.objects.get(qt_user_app_id=qt_user_app_id)
        except User.DoesNotExist as err:
            deprint(str(err))
            return Ret(Error.NOT_FOUND_USER)
        return Ret(o_user)

    @classmethod
    def create(cls, qt_user_app_id, token):
        ret = cls._validate(locals())
        if ret.error is not Error.OK:
            return ret

        ret = cls.get_user_by_qt_user_app_id(qt_user_app_id)
        if ret.error is Error.OK:
            o_user = ret.body
            o_user.qtb_token = token
            o_user.save()
            return Ret(o_user)
        try:
            o_user = cls(
                qt_user_app_id=qt_user_app_id,
                qtb_token=token,
                port=cls.get_unique_port(),
                ss_pwd=get_random_string(length=8),
                ss_on=False,
                ss_change_time=0,
            )
            o_user.save()
        except Exception as err:
            deprint(str(err))
            return Ret(Error.ERROR_CREATE_USER)

        o_user.do_ss_on()

        return Ret(o_user)

    def do_ss_on(self):
        if self.ss_on:
            return Ret()
        import datetime
        crt_time = datetime.datetime.now().timestamp()
        if crt_time - self.ss_change_time < self.SS_CHANGE_INTERVAL:
            return Ret(Error.SS_OPERATION_FAST)
        Dealer.add_port(self.port, self.ss_pwd)
        self.ss_on = True
        self.ss_change_time = crt_time
        self.save()
        return Ret()

    def do_ss_off(self):
        if not self.ss_on:
            return Ret()
        import datetime
        crt_time = datetime.datetime.now().timestamp()
        if crt_time - self.ss_change_time < self.SS_CHANGE_INTERVAL:
            return Ret(Error.SS_OPERATION_FAST)
        Dealer.remove_port(self.port)
        self.ss_on = False
        self.ss_change_time = crt_time
        self.save()
        return Ret()

    def do_ss_reset(self):
        import datetime
        crt_time = datetime.datetime.now().timestamp()
        if crt_time - self.ss_change_time < self.SS_CHANGE_INTERVAL:
            return Ret(Error.SS_OPERATION_FAST)

        if self.ss_on:
            Dealer.remove_port(self.port)
        self.port = self.get_unique_port()
        self.ss_pwd = get_random_string(length=8)
        Dealer.add_port(self.port, self.ss_pwd)

        self.ss_on = True
        self.ss_change_time = crt_time
        self.save()
        return Ret()

    @classmethod
    def get_user_by_id(cls, user_id):
        """根据用户ID获取用户对象"""
        try:
            o_user = cls.objects.get(pk=user_id)
        except cls.DoesNotExist as err:
            deprint(str(err))
            return Ret(Error.NOT_FOUND_USER)
        return Ret(o_user)

    @classmethod
    def get_user_by_port(cls, port):
        """根据用户分配的port获取用户对象"""
        try:
            o_user = cls.objects.get(port=port)
        except cls.DoesNotExist as err:
            deprint(str(err))
            return Ret(Error.NOT_FOUND_USER)
        return Ret(o_user)

    def to_dict(self):
        """把用户对象转换为字典"""
        return dict(
            port=self.port,
            ss_pwd=self.ss_pwd,
            nickname=self.nickname,
            avatar=self.avatar,
            ss_on=self.ss_on,
        )

    def update(self):
        from Base.qtb import update_user_info
        ret = update_user_info(self.qtb_token)
        if ret.error is not Error.OK:
            return ret
        body = ret.body
        self.avatar = body['avatar']
        self.nickname = body['nickname']
        self.description = body['description']
        self.save()
        return Ret()
