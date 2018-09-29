from Base.decorator import require_get, require_login, require_put
from Base.error import Error
from Base.jtoken import jwt_e
from Base.response import error_response, response, Ret
from User.models import User


def get_token_info(o_user):
    ret = jwt_e(dict(user_id=o_user.pk))
    if ret.error is not Error.OK:
        return ret
    token, dict_ = ret.body
    dict_['token'] = token
    return dict_


@require_get()
@require_login
def get_my_info(request):
    """ GET /api/user/

    获取我的信息
    """
    o_user = request.user
    return get_user_info(request, o_user.qt_user_app_id)


@require_get()
def get_user_info(request, qt_user_app_id):
    """ GET /api/user/@:qt_user_app_id

    获取用户信息
    """
    ret = User.get_user_by_qt_user_app_id(qt_user_app_id)
    if ret.error is not Error.OK:
        return error_response(ret)
    o_user = ret.body
    if not isinstance(o_user, User):
        return error_response(Error.STRANGE)
    o_user.update()
    return response(body=o_user.to_dict())


def validate_action(action):
    if action not in ['on', 'off', 'reset']:
        return Ret(Error.ERROR_PARAM_FORMAT, append_msg='，action取值错误')
    return Ret()


@require_put([('action', validate_action)])
@require_login
def change_ss(request):
    """ PUT /api/user/ss
    
    修改VPN信息
    """

    action = request.d.action

    o_user = request.user
    if not isinstance(o_user, User):
        return error_response(Error.STRANGE)

    print(action)
    if action == 'on':
        ret = o_user.do_ss_on()
    elif action == 'off':
        ret = o_user.do_ss_off()
    else:
        ret = o_user.do_ss_reset()

    if ret.error is not Error.OK:
        return error_response(ret)

    return response(body=o_user.to_dict())
