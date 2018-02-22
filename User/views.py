from Base.decorator import require_json, require_post, require_delete, require_login
from Base.error import Error
from Base.jtoken import jwt_e
from Base.response import error_response, response
from Config.models import Config
from User.models import User

ret_ = Config.get_config_by_key('beta-code')
if ret_.error is not Error.OK:
    excepted_bc = 'EXCEPTED_BC'
else:
    excepted_bc = ret_.body.value


def get_token_info(o_user):
    ret = jwt_e(dict(user_id=o_user.pk))
    if ret.error is not Error.OK:
        return error_response(ret)
    token, dict_ = ret.body
    dict_['token'] = token
    return dict_


@require_delete()
@require_login
def delete_user(request, username):
    """ DELETE /api/user/@:username

    删除用户
    """
    o_parent = request.user
    if not isinstance(o_parent, User):
        return error_response(Error.STRANGE)

    ret = User.get_user_by_username(username)
    if ret.error is not Error.OK:
        return error_response(ret)
    o_user = ret.body
    if not isinstance(o_user, User):
        return error_response(Error.STRANGE)
    if o_user.parent != o_parent or o_parent.pk == User.ROOT_ID:
        return error_response(Error.NO_DELETE_RIGHT)
    o_user.remove()
    return response()


@require_json
@require_post(['username', 'password', 'beta_code'])
# @require_login
def create_user(request):
    """ POST /api/user/

    创建用户
    """
    username = request.d.username
    password = request.d.password
    beta_code = request.d.beta_code

    if beta_code != excepted_bc:
        return error_response(Error.BETA_CODE_ERROR)

    # o_parent = request.user
    # if not isinstance(o_parent, User):
    #     return error_response(Error.STRANGE)
    ret = User.get_user_by_id(User.ROOT_ID)
    if ret.error is not Error.OK:
        return error_response(ret)
    o_parent = ret.body
    if not isinstance(o_parent, User):
        return error_response(Error.STRANGE)

    ret = User.create(username, password, o_parent)
    if ret.error is not Error.OK:
        return error_response(ret)
    o_user = ret.body
    if not isinstance(o_user, User):
        return error_response(Error.STRANGE)

    if ret.error is not Error.OK:
        return error_response(ret)

    return response(body=get_token_info(o_user))


@require_json
@require_post(['username', 'password'])
def auth_token(request):
    """ GET /api/user/token

    登录获取token
    """
    username = request.d.username
    password = request.d.password

    ret = User.authenticate(username, password)
    if ret.error != Error.OK:
        return error_response(ret)
    o_user = ret.body
    if not isinstance(o_user, User):
        return error_response(Error.STRANGE)

    return response(body=get_token_info(o_user))
