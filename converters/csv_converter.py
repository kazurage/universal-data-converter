"""
CSV конвертер
"""
import pandas as pd
import csv
from typing import Any, Union, List, Dict
import io
from .base import BaseConverter, ConversionError, ValidationError


class CSVConverter(BaseConverter):
    """Конвертер для CSV формата"""
    
    def __init__(self):
        super().__init__()
        self.supported_formats = ['csv']
    
    def parse(self, data: Union[str, bytes, io.IOBase]) -> Any:
        """Парсит CSV данные"""
        try:
            if isinstance(data, io.IOBase):
                df = pd.read_csv(data)
            elif isinstance(data, bytes):
                content = data.decode('utf-8')
                df = pd.read_csv(io.StringIO(content))
            else:
                df = pd.read_csv(io.StringIO(data))
            
            # Конвертируем DataFrame в список словарей
            return df.to_dict('records')
        except Exception as e:
            raise ConversionError(f"Ошибка парсинга CSV: {str(e)}")
    
    def serialize(self, data: Any) -> str:
        """Сериализует данные в CSV"""
        try:
            if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
                # Список словарей - стандартный формат
                df = pd.DataFrame(data)
            elif isinstance(data, dict):
                # Словарь - конвертируем в DataFrame
                if all(isinstance(v, list) for v in data.values()):
                    # Словарь списков
                    df = pd.DataFrame(data)
                else:
                    # Обычный словарь - делаем одну строку
                    df = pd.DataFrame([data])
            else:
                # Другие типы данных
                df = pd.DataFrame({'data': data if isinstance(data, list) else [data]})
            
            return df.to_csv(index=False)
        except Exception as e:
            raise ConversionError(f"Ошибка сериализации в CSV: {str(e)}")
    
    def validate(self, data: Union[str, bytes, io.IOBase]) -> bool:
        """Валидирует CSV данные"""
        try:
            if isinstance(data, io.IOBase):
                content = data.read()
                if isinstance(content, bytes):
                    content = content.decode('utf-8')
                data.seek(0)  # Возвращаем указатель в начало
            elif isinstance(data, bytes):
                content = data.decode('utf-8')
            else:
                content = data
            
            # Пробуем парсить как CSV
            csv.Sniffer().sniff(content)
            return True
        except Exception:
            return False
    
    def get_mime_type(self) -> str:
        return "text/csv"
    
    def get_file_extension(self) -> str:
        return ".csv"
