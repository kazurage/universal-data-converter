"""
JSON конвертер
"""
import json
from typing import Any, Union
import io
from .base import BaseConverter, ConversionError, ValidationError


class JSONConverter(BaseConverter):
    """Конвертер для JSON формата"""
    
    def __init__(self):
        super().__init__()
        self.supported_formats = ['json']
    
    def parse(self, data: Union[str, bytes, io.IOBase]) -> Any:
        """Парсит JSON данные"""
        try:
            if isinstance(data, io.IOBase):
                content = data.read()
                if isinstance(content, bytes):
                    content = content.decode('utf-8')
            elif isinstance(data, bytes):
                content = data.decode('utf-8')
            else:
                content = data
            
            return json.loads(content)
        except json.JSONDecodeError as e:
            raise ConversionError(f"Ошибка парсинга JSON: {str(e)}")
        except UnicodeDecodeError as e:
            raise ConversionError(f"Ошибка кодировки: {str(e)}")
    
    def serialize(self, data: Any) -> str:
        """Сериализует данные в JSON"""
        try:
            return json.dumps(data, ensure_ascii=False, indent=2)
        except (TypeError, ValueError) as e:
            raise ConversionError(f"Ошибка сериализации в JSON: {str(e)}")
    
    def validate(self, data: Union[str, bytes, io.IOBase]) -> bool:
        """Валидирует JSON данные"""
        try:
            self.parse(data)
            return True
        except ConversionError:
            return False
    
    def get_mime_type(self) -> str:
        return "application/json"
    
    def get_file_extension(self) -> str:
        return ".json"
