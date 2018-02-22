from Base.error import Error
from Base.response import Method, response, error_response
from User.views import create_user, auth_token


def rt_user(request):
    """ /api/user/

    # GET:    get_my_info, 获取我的信息
    POST:   create_user, 创建用户
    """
    options = {
        Method.GET: "获取我的信息",
        Method.POST: "创建用户",
    }
    if request.method == Method.OPTIONS:
        return response(body=options, allow=True)

    # if request.method == Method.GET:
    #     return get_my_info(request)
    if request.method == Method.POST:
        return create_user(request)
    return error_response(Error.ERROR_METHOD)


def rt_user_token(request):
    """ /api/user/token

    POST:   auth_token, 获取登录token
    """
    options = {
        Method.POST: "获取登录token"
    }
    if request.method == Method.OPTIONS:
        return response(body=options, allow=True)

    if request.method == Method.POST:
        return auth_token(request)
    return error_response(Error.ERROR_METHOD)
