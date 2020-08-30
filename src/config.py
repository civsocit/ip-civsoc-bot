"""Configuration module."""
import os


TOKEN = os.environ.get('TOKEN')


LOGGING_LEVEL = 'debug'  # Уровень логгирования
DIRECTORS_CHAT: int = None  # ID чата директората
REDACTION_CHAT: int = None  # ID чата редакции
