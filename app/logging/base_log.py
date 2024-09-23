"""
Модуль для настройки логирования приложения
BaseLoggings: класс, в котором есть основные функции для создания логов
"""
from loguru import logger


class BaseLoggings():
    """Класс, в котором лежат функции, для создания логов разной важности"""
    def __init__(self, *, 
        format: str = "{time} {level} {message}",
        file: str,
        rotation: str,
        level: str,
        serialize: bool = False
    ):
        """Инициализация объекта для логирования при помощи параметров"""
        logger.add(
            file, format=format, level=level, 
            rotation=rotation, compression="zip", serialize=serialize
        )
    
    # Создание функций для логирования в файл от меньшей степени важности до большей
    def debug(self, message):
        logger.debug(message)
    def info(self, message):
        logger.info(message)
    def warning(self, message):
        logger.warning(message)
    def error(self, message):
        logger.error(message)
    def critical(self, message):
        logger.critical(message)

# Объект для общих логов
log_app = BaseLoggings(file='logging/loggs_app/logging.log', rotation='100 MB', level='DEBUG')
# Объект для логов уровен которых выше ERROR (ошибка)
log_except = BaseLoggings(file='logging/loggs_app/except.log', rotation='100 MB', level='ERROR')
