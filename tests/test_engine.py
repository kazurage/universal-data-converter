"""
Тесты для движка конвертации
"""
import unittest
import json
from converters.engine import ConversionEngine, ConversionError


class TestConversionEngine(unittest.TestCase):
    """Тесты для движка конвертации"""
    
    def setUp(self):
        self.engine = ConversionEngine()
    
    def test_get_supported_formats(self):
        """Тест получения поддерживаемых форматов"""
        formats = self.engine.get_supported_formats()
        expected_formats = ['json', 'xml', 'csv', 'yaml', 'yml', 'toml']
        for fmt in expected_formats:
            self.assertIn(fmt, formats)
    
    def test_detect_format_json(self):
        """Тест автоопределения JSON формата"""
        json_data = '{"name": "test", "value": 123}'
        detected_format = self.engine.detect_format(json_data)
        self.assertEqual(detected_format, 'json')
    
    def test_detect_format_xml(self):
        """Тест автоопределения XML формата"""
        xml_data = '<root><name>test</name></root>'
        detected_format = self.engine.detect_format(xml_data)
        self.assertEqual(detected_format, 'xml')
    
    def test_detect_format_yaml(self):
        """Тест автоопределения YAML формата"""
        yaml_data = 'name: test\nvalue: 123\narray:\n  - item1\n  - item2'
        detected_format = self.engine.detect_format(yaml_data)
        self.assertEqual(detected_format, 'yaml')
    
    def test_detect_format_by_filename(self):
        """Тест автоопределения формата по имени файла"""
        json_data = '{"name": "test"}'
        detected_format = self.engine.detect_format(json_data, 'test.json')
        self.assertEqual(detected_format, 'json')
    
    def test_convert_json_to_yaml(self):
        """Тест конвертации из JSON в YAML"""
        json_data = '{"name": "test", "value": 123}'
        result = self.engine.convert(json_data, 'json', 'yaml')
        self.assertIn('name: test', result)
        self.assertIn('value: 123', result)
    
    def test_convert_yaml_to_json(self):
        """Тест конвертации из YAML в JSON"""
        yaml_data = 'name: test\nvalue: 123'
        result = self.engine.convert(yaml_data, 'yaml', 'json')
        parsed_result = json.loads(result)
        self.assertEqual(parsed_result['name'], 'test')
        self.assertEqual(parsed_result['value'], 123)
    
    def test_convert_same_format(self):
        """Тест конвертации в тот же формат"""
        json_data = '{"name": "test"}'
        result = self.engine.convert(json_data, 'json', 'json')
        self.assertEqual(result, json_data)
    
    def test_convert_auto_detect(self):
        """Тест конвертации с автоопределением исходного формата"""
        json_data = '{"name": "test", "value": 123}'
        result = self.engine.convert(json_data, 'auto', 'yaml')
        self.assertIn('name: test', result)
    
    def test_convert_unsupported_source_format(self):
        """Тест конвертации с неподдерживаемым исходным форматом"""
        with self.assertRaises(ConversionError):
            self.engine.convert('test', 'unsupported', 'json')
    
    def test_convert_unsupported_target_format(self):
        """Тест конвертации с неподдерживаемым целевым форматом"""
        with self.assertRaises(ConversionError):
            self.engine.convert('{"test": true}', 'json', 'unsupported')
    
    def test_validate_data_valid(self):
        """Тест валидации корректных данных"""
        json_data = '{"name": "test"}'
        self.assertTrue(self.engine.validate_data(json_data, 'json'))
    
    def test_validate_data_invalid(self):
        """Тест валидации некорректных данных"""
        invalid_json = '{"name": "test"'
        self.assertFalse(self.engine.validate_data(invalid_json, 'json'))
    
    def test_validate_data_unsupported_format(self):
        """Тест валидации с неподдерживаемым форматом"""
        self.assertFalse(self.engine.validate_data('test', 'unsupported'))
    
    def test_get_converter(self):
        """Тест получения конвертера по формату"""
        converter = self.engine.get_converter('json')
        self.assertIsNotNone(converter)
        self.assertEqual(converter.get_file_extension(), '.json')
    
    def test_get_converter_unsupported(self):
        """Тест получения конвертера для неподдерживаемого формата"""
        with self.assertRaises(ConversionError):
            self.engine.get_converter('unsupported')
    
    def test_get_mime_type(self):
        """Тест получения MIME типа"""
        mime_type = self.engine.get_mime_type('json')
        self.assertEqual(mime_type, 'application/json')
    
    def test_get_file_extension(self):
        """Тест получения расширения файла"""
        extension = self.engine.get_file_extension('json')
        self.assertEqual(extension, '.json')
    
    def test_complex_conversion_chain(self):
        """Тест сложной цепочки конвертации"""
        # JSON -> YAML -> JSON
        original_data = {"users": [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]}
        json_data = json.dumps(original_data)
        
        # JSON to YAML
        yaml_result = self.engine.convert(json_data, 'json', 'yaml')
        self.assertIn('users:', yaml_result)
        
        # YAML back to JSON
        json_result = self.engine.convert(yaml_result, 'yaml', 'json')
        parsed_result = json.loads(json_result)
        
        # Проверяем, что данные не изменились
        self.assertEqual(parsed_result, original_data)


if __name__ == '__main__':
    unittest.main()
