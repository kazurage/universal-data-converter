"""
YAML конвертер
"""
import yaml
from typing import Any, Union
import io
from .base import BaseConverter, ConversionError, ValidationError


class YAMLConverter(BaseConverter):
    """Конвертер для YAML формата"""
    
    def __init__(self):
        super().__init__()
        self.supported_formats = ['yaml', 'yml']
    
    def parse(self, data: Union[str, bytes, io.IOBase]) -> Any:
        """Парсит YAML данные"""
        try:
            if isinstance(data, io.IOBase):
                content = data.read()
                if isinstance(content, bytes):
                    content = content.decode('utf-8')
            elif isinstance(data, bytes):
                content = data.decode('utf-8')
            else:
                content = data
            
            return yaml.safe_load(content)
        except yaml.YAMLError as e:
            raise ConversionError(f"Ошибка парсинга YAML: {str(e)}")
        except UnicodeDecodeError as e:
            raise ConversionError(f"Ошибка кодировки: {str(e)}")
    
    def serialize(self, data: Any) -> str:
        """Сериализует данные в YAML"""
        try:
            return yaml.dump(data, default_flow_style=False, allow_unicode=True, indent=2)
        except yaml.YAMLError as e:
            raise ConversionError(f"Ошибка сериализации в YAML: {str(e)}")
    
    def validate(self, data: Union[str, bytes, io.IOBase]) -> bool:
        """Валидирует YAML данные"""
        try:
            self.parse(data)
            return True
        except ConversionError:
            return False
    
    def get_mime_type(self) -> str:
        return "application/x-yaml"
    
    def get_file_extension(self) -> str:
        return ".yaml"
