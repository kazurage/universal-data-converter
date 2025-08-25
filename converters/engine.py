"""
Универсальный движок конвертации
"""
from typing import Dict, Any, Union, Optional
import io
import os
from .base import BaseConverter, ConversionError, ValidationError
from .json_converter import JSONConverter
from .xml_converter import XMLConverter
from .csv_converter import CSVConverter
from .yaml_converter import YAMLConverter
from .toml_converter import TOMLConverter


class ConversionEngine:
    """Универсальный движок для конвертации между форматами"""
    
    def __init__(self):
        self.converters: Dict[str, BaseConverter] = {
            'json': JSONConverter(),
            'xml': XMLConverter(),
            'csv': CSVConverter(),
            'yaml': YAMLConverter(),
            'yml': YAMLConverter(),
            'toml': TOMLConverter()
        }
    
    def get_supported_formats(self) -> list:
        """Возвращает список поддерживаемых форматов"""
        return list(self.converters.keys())
    
    def detect_format(self, data: Union[str, bytes, io.IOBase], filename: Optional[str] = None) -> str:
        """Автоматически определяет формат данных"""
        # Получаем содержимое для проверки
        content = self._get_content_for_validation(data)
        
        # Сначала пробуем по расширению файла
        if filename:
            ext = os.path.splitext(filename)[1].lower().lstrip('.')
            if ext in self.converters:
                converter = self.converters[ext]
                try:
                    if converter.validate(content):
                        return ext
                except Exception:
                    pass
        
        # Если по расширению не получилось, пробуем валидацию для каждого формата
        for format_name, converter in self.converters.items():
            try:
                if converter.validate(content):
                    return format_name
            except Exception:
                continue
        
        raise ConversionError("Не удалось определить формат входных данных")
    
    def _get_content_for_validation(self, data: Union[str, bytes, io.IOBase]) -> str:
        """Получает содержимое данных для валидации"""
        if isinstance(data, io.IOBase):
            current_pos = data.tell()
            data.seek(0)
            content = data.read()
            data.seek(current_pos)  # Возвращаем указатель на место
            if isinstance(content, bytes):
                content = content.decode('utf-8')
            return content
        elif isinstance(data, bytes):
            return data.decode('utf-8')
        else:
            return data
    
    def convert(self, data: Union[str, bytes, io.IOBase], 
                source_format: str, target_format: str,
                filename: Optional[str] = None, stream: bool = False) -> str:
        """
        Конвертирует данные из одного формата в другой
        
        Args:
            data: Входные данные
            source_format: Исходный формат
            target_format: Целевой формат
            filename: Имя файла (для автоопределения формата)
            stream: Использовать потоковую обработку для больших файлов
            
        Returns:
            Строка с конвертированными данными
        """
        # Автоопределение исходного формата, если не указан
        if source_format == 'auto':
            source_format = self.detect_format(data, filename)
        
        # Проверяем поддержку форматов
        if source_format not in self.converters:
            raise ConversionError(f"Неподдерживаемый исходный формат: {source_format}")
        
        if target_format not in self.converters:
            raise ConversionError(f"Неподдерживаемый целевой формат: {target_format}")
        
        # Если форматы одинаковые, возвращаем исходные данные
        if source_format == target_format:
            if isinstance(data, io.IOBase):
                content = data.read()
                if isinstance(content, bytes):
                    return content.decode('utf-8')
                return content
            elif isinstance(data, bytes):
                return data.decode('utf-8')
            return data
        
        try:
            # Парсим исходные данные
            source_converter = self.converters[source_format]
            parsed_data = source_converter.parse(data)
            
            # Сериализуем в целевой формат
            target_converter = self.converters[target_format]
            result = target_converter.serialize(parsed_data)
            
            return result
            
        except Exception as e:
            raise ConversionError(f"Ошибка конвертации из {source_format} в {target_format}: {str(e)}")
    
    def validate_data(self, data: Union[str, bytes, io.IOBase], 
                     format_name: str) -> bool:
        """Валидирует данные для указанного формата"""
        if format_name not in self.converters:
            return False
        
        return self.converters[format_name].validate(data)
    
    def get_converter(self, format_name: str) -> BaseConverter:
        """Возвращает конвертер для указанного формата"""
        if format_name not in self.converters:
            raise ConversionError(f"Неподдерживаемый формат: {format_name}")
        
        return self.converters[format_name]
    
    def get_mime_type(self, format_name: str) -> str:
        """Возвращает MIME тип для формата"""
        converter = self.get_converter(format_name)
        return converter.get_mime_type()
    
    def get_file_extension(self, format_name: str) -> str:
        """Возвращает расширение файла для формата"""
        converter = self.get_converter(format_name)
        return converter.get_file_extension()
