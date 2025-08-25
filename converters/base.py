"""
Базовый класс для всех конвертеров
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Union
import io


class BaseConverter(ABC):
    """Базовый абстрактный класс для всех конвертеров"""
    
    def __init__(self):
        self.supported_formats = []
    
    @abstractmethod
    def parse(self, data: Union[str, bytes, io.IOBase]) -> Any:
        """Парсит данные из строки/байтов/файла в Python объект"""
        pass
    
    @abstractmethod
    def serialize(self, data: Any) -> str:
        """Сериализует Python объект в строку"""
        pass
    
    @abstractmethod
    def validate(self, data: Union[str, bytes, io.IOBase]) -> bool:
        """Валидирует входные данные"""
        pass
    
    def get_mime_type(self) -> str:
        """Возвращает MIME тип для формата"""
        return "text/plain"
    
    def get_file_extension(self) -> str:
        """Возвращает расширение файла для формата"""
        return ".txt"


class ConversionError(Exception):
    """Исключение для ошибок конвертации"""
    pass


class ValidationError(Exception):
    """Исключение для ошибок валидации"""
    pass
