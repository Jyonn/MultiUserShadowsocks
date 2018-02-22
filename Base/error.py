""" 171203 Adel Liu

错误表，在编码时不断添加
"""


class Error:
    NOT_FOUND_USER = 2006
    ERROR_PASSWORD = 2005
    ERROR_CREATE_USER = 2004
    USERNAME_EXIST = 2003
    REQUIRE_GRANT = 2002
    INVALID_PASSWORD = 2001
    INVALID_USERNAME = 2000

    BETA_CODE_ERROR = 1012
    ERROR_PROCESS_FUNC = 1011
    ERROR_TUPLE_FORMAT = 1010
    REQUIRE_ROOT = 1009
    ERROR_VALIDATION_FUNC = 1008
    ERROR_PARAM_FORMAT = 1007
    REQUIRE_BASE64 = 1006
    ERROR_METHOD = 1005
    STRANGE = 1004
    REQUIRE_LOGIN = 1003
    REQUIRE_JSON = 1002
    REQUIRE_PARAM = 1001
    ERROR_NOT_FOUND = 1000
    OK = 0

    ERROR_DICT = [
        (NOT_FOUND_USER, "不存在的用户"),
        (ERROR_PASSWORD, "错误的用户名或密码"),
        (ERROR_CREATE_USER, "创建用户失败"),
        (USERNAME_EXIST, "已存在的用户"),
        (REQUIRE_GRANT, "改用户无权限操作"),
        (INVALID_PASSWORD, "密码长度应在6-16个字符之内且无非法字符"),
        (INVALID_USERNAME, "用户名只能是包含字母数字和下划线的3-32位字符串"),

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
