import os
from typing import Optional, Union


class Config:
    _fields = ['TOKEN', 'WEBHOOK_HOST', 'WEBHOOK_PATH', 'PORT',
               'DIRECTORS_CHAT', 'REDACTION_CHAT',
               'REDIS_HOST', 'REDIS_PORT', 'REDIS_INDEX', 'REDIS_PASS',
               'LOG_LEVEL']

    TOKEN: str
    WEBHOOK_HOST: str
    WEBHOOK_PATH: str
    PORT: int
    DIRECTORS_CHAT: int
    REDATCION_CHAT: int
    REDIS_HOST: Optional[str]
    REDIS_PORT: Optional[int]
    REDIS_INDEX: int
    REDIS_PASS: Optional[str]
    LOG_LEVEL: str

    @classmethod
    def from_env(cls):
        dictionary = {}
        for field in cls._fields:
            field_result = os.environ.get(field)
            if field_result:
                dictionary[field.lower()] = field_result
        return cls(**dictionary)

    def __init__(self,
                 token: str,
                 webhook_host: str,
                 directors_chat: Union[int, str],
                 redaction_chat: Union[int, str],
                 webhook_path: str = '/',
                 port: Union[int, str] = 80,
                 redis_host: Optional[str] = None,
                 redis_port: Optional[int] = None,
                 redis_index: Optional[int] = None,
                 redis_pass: Optional[str] = None,
                 log_level: str = 'INFO'):
        self.TOKEN = token
        self.WEBHOOK_HOST = webhook_host
        self.WEBHOOK_PATH = webhook_path
        self.PORT = int(port)
        self.DIRECTORS_CHAT = int(directors_chat)
        self.REDACTION_CHAT = int(redaction_chat)
        self.REDIS_HOST = redis_host
        self.REDIS_PORT = redis_port
        self.REDIS_INDEX = redis_index
        self.REDIS_PASS = redis_pass
        self.LOG_LEVEL = self._validate_log_level(log_level)

    def _validate_log_level(self, log_level: str) -> str:
        log_level = log_level.upper()
        if log_level not in ('CRITICAL',
                             'ERROR',
                             'WARNING',
                             'INFO',
                             'DEBUG',
                             'NOTSET'):
            raise ValueError('Invalid logging level.')
        return log_level
