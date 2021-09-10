""" Adel Liu 180221

用户类
"""
import random

from SmartDjango import models, E, P
from django.utils.crypto import get_random_string

from Base.common import qt_manager
from Base.dealer import Dealer


@E.register(id_processor=E.idp_cls_prefix())
class UserError:
    NOT_FOUND = E("找不到用户", hc=404)
    CREATE = E("创建用户失败", hc=400)
    SS_OPERATION_FAST = E("对VPN帐号操作频率过快，请间隔五分钟")
    ACTION = E("错误的命令")


class User(models.Model):
    """
    用户类
    根超级用户id=1
    """
    ROOT_ID = 1
    SS_CHANGE_INTERVAL = 300

    avatar = models.CharField(
        default=None,
        null=True,
        blank=True,
        max_length=1024,
    )
    nickname = models.CharField(
        max_length=10,
        default=None,
        blank=True,
        null=True,
    )
    qt_user_app_id = models.CharField(
        default=None,
        max_length=16,
    )
    qtb_token = models.CharField(
        default=None,
        max_length=256,
    )
    description = models.CharField(
        max_length=20,
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
        max_length=32,
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

    @classmethod
    def get_unique_port(cls):
        while True:
            port = random.randint(60000, 65500)
            try:
                cls.get_by_port(port)
            except E as e:
                if e.eis(UserError.NOT_FOUND):
                    return port
                else:
                    raise e

    @staticmethod
    def get_by_qt(qt_user_app_id):
        """根据齐天用户-应用ID获取用户对象"""
        try:
            return User.objects.get(qt_user_app_id=qt_user_app_id)
        except User.DoesNotExist as err:
            raise UserError.NOT_FOUND(debug_message=err)

    @classmethod
    def create(cls, qt_user_app_id, token):

        try:
            user = cls.get_by_qt(qt_user_app_id)
            user.qtb_token = token
            user.save()
        except E as e:
            if e.eis(UserError.NOT_FOUND):
                try:
                    user = cls.objects.create(
                        qt_user_app_id=qt_user_app_id,
                        qtb_token=token,
                        port=cls.get_unique_port(),
                        ss_pwd=get_random_string(length=8),
                        ss_on=False,
                        ss_change_time=0,
                    )
                except Exception as err:
                    raise UserError.CREATE(debug_message=err)
            else:
                raise e

        user.do_ss_on()
        return user

    def do_ss_on(self):
        if self.ss_on:
            return
        import datetime
        crt_time = datetime.datetime.now().timestamp()
        if crt_time - self.ss_change_time < self.SS_CHANGE_INTERVAL:
            raise UserError.SS_OPERATION_FAST
        Dealer.add_port(self.port, self.ss_pwd)
        self.ss_on = True
        self.ss_change_time = crt_time
        self.save()

    def do_ss_off(self):
        if not self.ss_on:
            return
        import datetime
        crt_time = datetime.datetime.now().timestamp()
        if crt_time - self.ss_change_time < self.SS_CHANGE_INTERVAL:
            raise UserError.SS_OPERATION_FAST
        Dealer.remove_port(self.port)
        self.ss_on = False
        self.ss_change_time = crt_time
        self.save()

    def do_ss_reset(self):
        import datetime
        crt_time = datetime.datetime.now().timestamp()
        if crt_time - self.ss_change_time < self.SS_CHANGE_INTERVAL:
            raise UserError.SS_OPERATION_FAST

        if self.ss_on:
            Dealer.remove_port(self.port)
        self.port = self.get_unique_port()
        self.ss_pwd = get_random_string(length=8)
        Dealer.add_port(self.port, self.ss_pwd)

        self.ss_on = True
        self.ss_change_time = crt_time
        self.save()

    @classmethod
    def get_by_id(cls, user_id):
        """根据用户ID获取用户对象"""
        try:
            return cls.objects.get(pk=user_id)
        except cls.DoesNotExist as err:
            raise UserError.NOT_FOUND(debug_message=err)

    @classmethod
    def get_by_port(cls, port):
        """根据用户分配的port获取用户对象"""
        try:
            return cls.objects.get(port=port)
        except cls.DoesNotExist as err:
            raise UserError.NOT_FOUND(debug_message=err)

    def d(self):
        """把用户对象转换为字典"""
        return self.dictify('port', 'ss_pwd', 'nickname', 'avatar', 'ss_on')

    def update(self):
        body = qt_manager.get_user_info(self.qtb_token)
        self.avatar = body['avatar']
        self.nickname = body['nickname']
        self.description = body['description']
        self.save()


class UserP:
    @staticmethod
    def action_validator(action):
        if action not in ['on', 'off', 'reset']:
            raise UserError.ACTION

    action = P('action').validate(action_validator)
