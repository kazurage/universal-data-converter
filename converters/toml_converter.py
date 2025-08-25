"""
TOML конвертер
"""
import toml
from typing import Any, Union
import io
from .base import BaseConverter, ConversionError, ValidationError


class TOMLConverter(BaseConverter):
    """Конвертер для TOML формата"""
    
    def __init__(self):
        super().__init__()
        self.supported_formats = ['toml']
    
    def parse(self, data: Union[str, bytes, io.IOBase]) -> Any:
        """Парсит TOML данные"""
        try:
            if isinstance(data, io.IOBase):
                content = data.read()
                if isinstance(content, bytes):
                    content = content.decode('utf-8')
            elif isinstance(data, bytes):
                content = data.decode('utf-8')
            else:
                content = data
            
            return toml.loads(content)
        except toml.TomlDecodeError as e:
            raise ConversionError(f"Ошибка парсинга TOML: {str(e)}")
        except UnicodeDecodeError as e:
            raise ConversionError(f"Ошибка кодировки: {str(e)}")
    
    def serialize(self, data: Any) -> str:
        """Сериализует данные в TOML"""
        try:
            if not isinstance(data, dict):
                # TOML требует словарь верхнего уровня
                data = {"data": data}
            return toml.dumps(data)
        except Exception as e:
            raise ConversionError(f"Ошибка сериализации в TOML: {str(e)}")
    
    def validate(self, data: Union[str, bytes, io.IOBase]) -> bool:
        """Валидирует TOML данные"""
        try:
            self.parse(data)
            return True
        except ConversionError:
            return False
    
    def get_mime_type(self) -> str:
        return "application/toml"
    
    def get_file_extension(self) -> str:
        return ".toml"
