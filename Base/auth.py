from functools import wraps

from Base.jtoken import JWT
from SmartDjango import E

from User.models import User


@E.register(id_processor=E.idp_cls_prefix())
class AuthError:
    REQUIRE_ROOT = E("需要管理员权限", hc=401)
    REQUIRE_RIGHT = E("需要{0}权限", hc=401)
    EXPIRED = E("登录过期", hc=401)
    REQUIRE_ADMIN = E("需要管理员登录", hc=401)
    REQUIRE_USER = E("需要登录", hc=401)
    TOKEN_MISS_PARAM = E("认证口令缺少参数{0}", hc=400)
    REQUIRE_LOGIN = E("需要登录", hc=401)


class Auth:
    @staticmethod
    def validate_token(r):
        jwt_str = r.META.get('HTTP_TOKEN')
        if jwt_str is None:
            raise AuthError.REQUIRE_LOGIN
        return JWT.decrypt(jwt_str)

    @staticmethod
    def get_login_token(user: User):
        token, _dict = JWT.encrypt(dict(
            user_id=user.pk,
        ), expire_second=30 * 60 * 60 * 24)
        _dict['token'] = token
        _dict['user'] = user.d()
        return _dict

    @classmethod
    def _extract_user(cls, r):
        r.user = None

        dict_ = Auth.validate_token(r)
        user_id = dict_.get('user_id')
        if not user_id:
            raise AuthError.TOKEN_MISS_PARAM('user_id')

        from User.models import User
        r.user = User.get_by_id(user_id)

    @staticmethod
    def maybe_login(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            try:
                Auth._extract_user(request)
            except E:
                pass
            return func(request, *args, **kwargs)

        return wrapper

    @classmethod
    def require_login(cls, func):
        @wraps(func)
        def wrapper(r, *args, **kwargs):
            cls._extract_user(r)
            return func(r, *args, **kwargs)

        return wrapper
