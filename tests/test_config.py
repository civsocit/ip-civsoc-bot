import os

import pytest

from ip_bot.config import Config


class TestLogLevelValidation:
    def test_invalid(self):
        with pytest.raises(ValueError):
            Config('qwerty', 123, 123, log_level='qwerty')

    @pytest.mark.parametrize('input_level,output_level', [
        ('debug', 'DEBUG'),
        ('INFO', 'INFO')
    ])
    def test_valid(self, input_level: str, output_level: str):
        config = Config('qwerty', 123, 123, log_level=input_level)
        assert config.LOG_LEVEL == output_level


def test_from_env():
    data = {'TOKEN': 'qwerty',
            'DIRECTORS_CHAT': '123',
            'REDACTION_CHAT': '123',
            'LOG_LEVEL': 'DEBUG'}
    for key in data.keys():
        os.environ[key] = data[key]
    config = Config.from_env()
    config_dict = {}
    for key in data.keys():
        config_dict[key] = str(getattr(config, key))
        del os.environ[key]
    assert config_dict == data
