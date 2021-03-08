from starlette import status


class CommonException(Exception):
    code: int
    message: str

    def __str__(self):
        return self.code, self.message

    def __iter__(self):
        yield from [self.code, self.message]

    # 常见 status-code:
    # 200: 服务器成功返回用户请求的数据。
    # 400: 用户发出的请求有错误，服务器没有进行新建或修改数据的操作，该操作是幂等的。
    # 401: 表示用户没有权限（令牌、用户名、密码错误）。
    # 403: 表示用户得到授权（与 401 错误相对），但是访问是被禁止的。
    # 404: 用户发出的请求针对的是不存在的记录（或爬取解析失败），服务器没有进行操作，该操作是幂等的。
    # 500: 服务器发生错误，用户将无法判断发出的请求是否成功。


class FormException(CommonException):
    # 用户提交的表单有误（来源于用户的不可信表单，不应该被 sentry 捕获）
    def __init__(self, message):
        self.code = status.HTTP_400_BAD_REQUEST
        self.message = message


class NetworkException(CommonException):
    # 代表客户端、服务器、教务服务器之间网络不通畅
    def __init__(self, message):
        self.code = status.HTTP_500_INTERNAL_SERVER_ERROR
        self.message = message


class AccessException(CommonException):
    # 爬虫服务器访问教务在线出问题（非网络问题），可能是回话过期
    def __init__(self, message):
        self.code = status.HTTP_403_FORBIDDEN
        self.message = message


class SpiderParserException(CommonException):
    # 爬虫解析出错
    def __init__(self, message):
        self.code = status.HTTP_404_NOT_FOUND
        self.message = message


class TokenException(CommonException):
    # TODO, JWT
    def __init__(self, message):
        self.code = status.HTTP_401_UNAUTHORIZED
        self.message = message
