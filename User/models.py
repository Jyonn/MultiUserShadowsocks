""" Adel Liu 180221

用户类
"""
import re

from django.db import models

from Base.common import deprint
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
        'username': 32,
        'password': 32,
        'ss_pwd': 32,
    }
    username = models.CharField(
        max_length=L['username'],
        unique=True,
    )
    password = models.CharField(
        max_length=L['password'],
    )
    pwd_change_time = models.FloatField(
        null=True,
        blank=True,
        default=0,
    )
    parent = models.ForeignKey(
        'User',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    grant = models.BooleanField(
        verbose_name='是否有权限新增用户',
        default=False,
    )
    port = models.SmallIntegerField(
        verbose_name='SS端口',
        default=0,
        unique=True,
    )
    ss_pwd = models.CharField(
        verbose_name='SS密码',
        default=None,
        max_length=L['ss_pwd'],
    )
    FIELD_LIST = ['username', 'password', 'parent', 'grant', 'port', 'ss_pwd']

    @staticmethod
    def _valid_username(username):
        """验证用户名合法"""
        valid_chars = '^[A-Za-z0-9_]{3,32}$'
        if re.match(valid_chars, username) is None:
            return Ret(Error.INVALID_USERNAME)
        return Ret()

    @staticmethod
    def _valid_password(password):
        """验证密码合法"""
        valid_chars = '^[A-Za-z0-9!@#$%^&*()_+-=,.?;:]{6,16}$'
        if re.match(valid_chars, password) is None:
            return Ret(Error.INVALID_PASSWORD)
        return Ret()

    @staticmethod
    def _valid_o_parent(o_parent):
        """验证o_parent合法"""
        if not isinstance(o_parent, User):
            return Ret(Error.STRANGE)
        if not o_parent.grant:
            return Ret(Error.REQUIRE_GRANT)
        return Ret()

    @classmethod
    def _validate(cls, dict_):
        """验证传入参数是否合法"""
        return field_validator(dict_, cls)

    @classmethod
    def create(cls, username, password, o_parent):
        """ 创建用户

        :param username: 用户名
        :param password: 密码
        :param o_parent: 父用户
        :return: Ret对象，错误返回错误代码，成功返回用户对象
        """
        ret = cls._validate(locals())
        if ret.error is not Error.OK:
            return ret

        hash_password = User._hash(password)
        ret = User.get_user_by_username(username)
        if ret.error is Error.OK:
            return Ret(Error.USERNAME_EXIST)
        try:
            o_user = cls(
                username=username,
                password=hash_password,
                email=None,
                parent=o_parent,
                avatar=None,
                grant=False,
                nickname='',
            )
            o_user.save()
        except ValueError as err:
            deprint(str(err))
            return Ret(Error.ERROR_CREATE_USER)
        return Ret(o_user)

    def change_password(self, password, old_password):
        """修改密码"""
        ret = self._validate(locals())
        if ret.error is not Error.OK:
            return ret
        if self.password != User._hash(old_password):
            return Ret(Error.ERROR_PASSWORD)
        hash_password = User._hash(password)
        self.password = hash_password
        import datetime
        self.pwd_change_time = datetime.datetime.now().timestamp()
        self.save()
        return Ret()

    @staticmethod
    def _hash(s):
        from Base.common import md5
        return md5(s)

    @staticmethod
    def get_user_by_username(username):
        """根据用户名获取用户对象"""
        try:
            o_user = User.objects.get(username=username)
        except User.DoesNotExist as err:
            deprint(str(err))
            return Ret(Error.NOT_FOUND_USER)
        return Ret(o_user)

    @staticmethod
    def get_user_by_id(user_id):
        """根据用户ID获取用户对象"""
        try:
            o_user = User.objects.get(pk=user_id)
        except User.DoesNotExist as err:
            deprint(str(err))
            return Ret(Error.NOT_FOUND_USER)
        return Ret(o_user)

    def to_dict(self):
        """把用户对象转换为字典"""
        return dict(
            username=self.username,
        )

    @staticmethod
    def authenticate(username, password):
        """验证用户名和密码是否匹配"""
        ret = User._validate(locals())
        if ret.error is not Error.OK:
            return ret
        try:
            o_user = User.objects.get(username=username)
        except User.DoesNotExist as err:
            deprint(str(err))
            return Ret(Error.NOT_FOUND_USER)
        if User._hash(password) == o_user.password:
            return Ret(o_user)
        return Ret(Error.ERROR_PASSWORD)
