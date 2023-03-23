from enum import Enum, unique

@unique
class Config(Enum):
    log_file = 'a.log'
    account = "winger"
    user_email = "test@qq.com"

    api_key = ''

    ## 接口相关
    openai_max_tokens = 4096
    limit_max_tokens = 1000
    output_language = 'chinese'


conf = Config()