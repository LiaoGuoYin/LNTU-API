from enum import Enum


class StatusCodeEnum(Enum):
    # 200: 服务器成功返回用户请求的数据。
    # 400: 用户发出的请求有错误，服务器没有进行新建或修改数据的操作，该操作是幂等的。
    # 401: 表示用户没有权限（令牌、用户名、密码错误）。
    # 403: 表示用户得到授权（与 401 错误相对），但是访问是被禁止的。
    # 404: 用户发出的请求针对的是不存在的记录(或爬取解析失败)，服务器没有进行操作，该操作是幂等的。
    # 500: 服务器发生错误，用户将无法判断发出的请求是否成功。
    SUCCESS = 200
    INVALID_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    SERVER_INTERNAL_ERROR = 500


class CommonException(Exception):
    code: StatusCodeEnum
    msg: str

    def __str__(self):
        return self.code, self.msg

    def __iter__(self):
        yield from [self.code, self.msg]


class TokenException(CommonException):
    def __init__(self, msg):
        self.code = StatusCodeEnum.UNAUTHORIZED
        self.msg = msg


class FormException(CommonException):
    def __init__(self, msg):
        self.code = StatusCodeEnum.INVALID_REQUEST
        self.msg = msg


class AccessException(CommonException):
    def __init__(self, msg):
        self.code = StatusCodeEnum.FORBIDDEN  # 访问教务服务器网络失败
        self.msg = msg


class SpiderParserException(CommonException):
    def __init__(self, msg):
        self.code = StatusCodeEnum.NOT_FOUND
        self.msg = msg


class NetworkException(CommonException):
    def __init__(self, msg):
        self.code = StatusCodeEnum.SERVER_INTERNAL_ERROR  # 代表客户端，服务器，教务服务器之间网络不通畅
        self.msg = msg
