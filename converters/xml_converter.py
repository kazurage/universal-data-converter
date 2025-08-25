"""
XML конвертер
"""
import xmltodict
import xml.etree.ElementTree as ET
from typing import Any, Union, Dict
import io
from .base import BaseConverter, ConversionError, ValidationError


class XMLConverter(BaseConverter):
    """Конвертер для XML формата"""
    
    def __init__(self):
        super().__init__()
        self.supported_formats = ['xml']
    
    def parse(self, data: Union[str, bytes, io.IOBase]) -> Any:
        """Парсит XML данные"""
        try:
            if isinstance(data, io.IOBase):
                content = data.read()
                if isinstance(content, bytes):
                    content = content.decode('utf-8')
            elif isinstance(data, bytes):
                content = data.decode('utf-8')
            else:
                content = data
            
            return xmltodict.parse(content)
        except Exception as e:
            raise ConversionError(f"Ошибка парсинга XML: {str(e)}")
    
    def serialize(self, data: Any) -> str:
        """Сериализует данные в XML"""
        try:
            return self._dict_to_xml(data)
        except Exception as e:
            raise ConversionError(f"Ошибка сериализации в XML: {str(e)}")
    
    def _dict_to_xml(self, data: Any, indent: str = "") -> str:
        """Преобразует данные в XML без корневого элемента"""
        if isinstance(data, dict):
            result = []
            for key, value in data.items():
                if isinstance(value, dict):
                    result.append(f"{indent}<{key}>")
                    result.append(self._dict_to_xml(value, indent + "\t"))
                    result.append(f"{indent}</{key}>")
                elif isinstance(value, list):
                    for item in value:
                        result.append(f"{indent}<{key}>")
                        if isinstance(item, (dict, list)):
                            result.append(self._dict_to_xml(item, indent + "\t"))
                        else:
                            result.append(f"{indent}\t{self._escape_xml(str(item))}")
                        result.append(f"{indent}</{key}>")
                else:
                    result.append(f"{indent}<{key}>{self._escape_xml(str(value))}</{key}>")
            return "\n".join(result)
        elif isinstance(data, list):
            result = []
            for item in data:
                result.append(f"{indent}<item>")
                if isinstance(item, (dict, list)):
                    result.append(self._dict_to_xml(item, indent + "\t"))
                else:
                    result.append(f"{indent}\t{self._escape_xml(str(item))}")
                result.append(f"{indent}</item>")
            return "\n".join(result)
        else:
            return self._escape_xml(str(data))
    
    def _escape_xml(self, text: str) -> str:
        """Экранирует специальные символы XML"""
        return (text.replace("&", "&amp;")
                   .replace("<", "&lt;")
                   .replace(">", "&gt;")
                   .replace('"', "&quot;")
                   .replace("'", "&apos;"))
    
    def validate(self, data: Union[str, bytes, io.IOBase]) -> bool:
        """Валидирует XML данные"""
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
            
            ET.fromstring(content)
            return True
        except ET.ParseError:
            return False
        except Exception:
            return False
    
    def get_mime_type(self) -> str:
        return "application/xml"
    
    def get_file_extension(self) -> str:
        return ".xml"
