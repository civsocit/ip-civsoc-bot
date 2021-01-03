import os
from typing import Optional, Union


class Config:
    _fields = ['TOKEN', 'DIRECTORS_CHAT', 'REDACTION_CHAT', 'WEBHOOK_URL',
               'REDIS_HOST', 'REDIS_PORT', 'REDIS_INDEX', 'REDIS_PASS',
               'LOG_LEVEL']

    TOKEN: str
    WEBHOOK_URL: str
    DIRECTORS_CHAT: int
    REDATCION_CHAT: int
    REDIS_HOST: Optional[str]
    REDIS_PORT: Optional[int]
    REDIS_INDEX: int = 0
    REDIS_PASS: Optional[str]
    LOG_LEVEL: str = 'DEBUG'

    @classmethod
    def from_env(cls):
        dictionary = {}
        for field in cls._fields:
            dictionary[field.lower()] = os.environ.get(field)
        return cls(**dictionary)

    def __init__(self,
                 token: str,
                 webhook_url: str,
                 directors_chat: Union[int, str],
                 redaction_chat: Union[int, str],
                 redis_host: Optional[str] = None,
                 redis_port: Optional[int] = None,
                 redis_index: int = 0,
                 redis_pass: Optional[str] = None,
                 log_level: Optional[str] = None):
        self.TOKEN = token
        self.WEBHOOK_URL = webhook_url
        self.DIRECTORS_CHAT = int(directors_chat)
        self.REDACTION_CHAT = int(redaction_chat)
        self.REDIS_HOST = redis_host
        self.REDIS_PORT = redis_port
        self.REDIS_INDEX = redis_index
        self.REDIS_PASS = redis_pass
        if log_level:
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
