import os
from typing import Optional, Union


class Config:
    _fields = ['TOKEN', 'LOG_LEVEL', 'DIRECTORS_CHAT', 'REDACTION_CHAT']

    TOKEN: str
    LOG_LEVEL: str = 'DEBUG'
    DIRECTORS_CHAT: int
    REDATCION_CHAT: int

    @classmethod
    def from_env(cls):
        dictionary = {}
        for field in cls._fields:
            dictionary[field.lower()] = os.environ.get(field)
        return cls(**dictionary)

    def __init__(self,
                 token: str,
                 directors_chat: Union[int, str],
                 redaction_chat: Union[int, str],
                 log_level: Optional[str] = None):
        self.TOKEN = token
        self.DIRECTORS_CHAT = int(directors_chat)
        self.REDACTION_CHAT = int(redaction_chat)
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
