""" 180222 Adel Liu

错误表，在编码时不断添加
"""


class E:
    def __init__(self, error_id):
        self.eid = error_id


class Error:
    NO_DELETE_RIGHT = E(2008)
    NOT_FOUND_CONFIG = E(2007)
    NOT_FOUND_USER = E(2006)
    ERROR_PASSWORD = E(2005)
    ERROR_CREATE_USER = E(2004)
    USERNAME_EXIST = E(2003)
    REQUIRE_GRANT = E(2002)
    INVALID_PASSWORD = E(2001)
    INVALID_USERNAME = E(2000)

    PASSWORD_CHANGED = E(1013)
    BETA_CODE_ERROR = E(1012)
    ERROR_PROCESS_FUNC = E(1011)
    ERROR_TUPLE_FORMAT = E(1010)
    REQUIRE_ROOT = E(1009)
    ERROR_VALIDATION_FUNC = E(1008)
    ERROR_PARAM_FORMAT = E(1007)
    REQUIRE_BASE64 = E(1006)
    ERROR_METHOD = E(1005)
    STRANGE = E(1004)
    REQUIRE_LOGIN = E(1003)
    REQUIRE_JSON = E(1002)
    REQUIRE_PARAM = E(1001)
    ERROR_NOT_FOUND = E(1000)
    OK = E(0)

    ERROR_DICT = [
        (NO_DELETE_RIGHT, "没有删除权限"),
        (NOT_FOUND_CONFIG, "不存在的配置"),
        (NOT_FOUND_USER, "不存在的用户"),
        (ERROR_PASSWORD, "错误的用户名或密码"),
        (ERROR_CREATE_USER, "创建用户失败"),
        (USERNAME_EXIST, "已存在的用户"),
        (REQUIRE_GRANT, "改用户无权限操作"),
        (INVALID_PASSWORD, "密码长度应在6-16个字符之内且无非法字符"),
        (INVALID_USERNAME, "用户名只能是包含字母数字和下划线的3-32位字符串"),

        (PASSWORD_CHANGED, "密码已改变，需要重新获取token"),
        (BETA_CODE_ERROR, "内测码错误"),
        (ERROR_PROCESS_FUNC, "参数预处理函数错误"),
        (ERROR_TUPLE_FORMAT, "属性元组格式错误"),
        (REQUIRE_ROOT, "需要管理员登录"),
        (ERROR_VALIDATION_FUNC, "错误的参数验证函数"),
        (ERROR_PARAM_FORMAT, "错误的参数格式"),
        (REQUIRE_BASE64, "参数需要base64编码"),
        (ERROR_METHOD, "错误的HTTP请求方法"),
        (STRANGE, "未知错误"),
        (REQUIRE_LOGIN, "需要登录"),
        (REQUIRE_JSON, "需要JSON数据"),
        (REQUIRE_PARAM, "缺少参数"),
        (ERROR_NOT_FOUND, "不存在的错误"),
        (OK, "没有错误"),
    ]
