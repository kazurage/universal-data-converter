"""
Тесты для модулей конвертации
"""
import unittest
import json
import io
from converters.json_converter import JSONConverter
from converters.xml_converter import XMLConverter
from converters.csv_converter import CSVConverter
from converters.yaml_converter import YAMLConverter
from converters.toml_converter import TOMLConverter
from converters.base import ConversionError


class TestJSONConverter(unittest.TestCase):
    """Тесты для JSON конвертера"""
    
    def setUp(self):
        self.converter = JSONConverter()
    
    def test_parse_valid_json(self):
        """Тест парсинга корректного JSON"""
        json_data = '{"name": "test", "value": 123}'
        result = self.converter.parse(json_data)
        self.assertEqual(result, {"name": "test", "value": 123})
    
    def test_parse_invalid_json(self):
        """Тест парсинга некорректного JSON"""
        invalid_json = '{"name": "test", "value":}'
        with self.assertRaises(ConversionError):
            self.converter.parse(invalid_json)
    
    def test_serialize_dict(self):
        """Тест сериализации словаря в JSON"""
        data = {"name": "test", "value": 123}
        result = self.converter.serialize(data)
        self.assertIn('"name": "test"', result)
        self.assertIn('"value": 123', result)
    
    def test_validate_valid_json(self):
        """Тест валидации корректного JSON"""
        json_data = '{"name": "test"}'
        self.assertTrue(self.converter.validate(json_data))
    
    def test_validate_invalid_json(self):
        """Тест валидации некорректного JSON"""
        invalid_json = '{"name": "test"'
        self.assertFalse(self.converter.validate(invalid_json))


class TestXMLConverter(unittest.TestCase):
    """Тесты для XML конвертера"""
    
    def setUp(self):
        self.converter = XMLConverter()
    
    def test_parse_valid_xml(self):
        """Тест парсинга корректного XML"""
        xml_data = '<root><name>test</name><value>123</value></root>'
        result = self.converter.parse(xml_data)
        self.assertIn('root', result)
    
    def test_serialize_dict(self):
        """Тест сериализации словаря в XML"""
        data = {"root": {"name": "test", "value": 123}}
        result = self.converter.serialize(data)
        self.assertIn('<root>', result)
        self.assertIn('<name>test</name>', result)
    
    def test_validate_valid_xml(self):
        """Тест валидации корректного XML"""
        xml_data = '<root><name>test</name></root>'
        self.assertTrue(self.converter.validate(xml_data))
    
    def test_validate_invalid_xml(self):
        """Тест валидации некорректного XML"""
        invalid_xml = '<root><name>test</root>'
        self.assertFalse(self.converter.validate(invalid_xml))


class TestCSVConverter(unittest.TestCase):
    """Тесты для CSV конвертера"""
    
    def setUp(self):
        self.converter = CSVConverter()
    
    def test_parse_valid_csv(self):
        """Тест парсинга корректного CSV"""
        csv_data = 'name,value\ntest,123\ntest2,456'
        result = self.converter.parse(csv_data)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['name'], 'test')
        self.assertEqual(result[0]['value'], 123)
    
    def test_serialize_list_of_dicts(self):
        """Тест сериализации списка словарей в CSV"""
        data = [{"name": "test", "value": 123}, {"name": "test2", "value": 456}]
        result = self.converter.serialize(data)
        self.assertIn('name,value', result)
        self.assertIn('test,123', result)
    
    def test_serialize_dict(self):
        """Тест сериализации словаря в CSV"""
        data = {"name": "test", "value": 123}
        result = self.converter.serialize(data)
        self.assertIn('name,value', result)
        self.assertIn('test,123', result)


class TestYAMLConverter(unittest.TestCase):
    """Тесты для YAML конвертера"""
    
    def setUp(self):
        self.converter = YAMLConverter()
    
    def test_parse_valid_yaml(self):
        """Тест парсинга корректного YAML"""
        yaml_data = 'name: test\nvalue: 123'
        result = self.converter.parse(yaml_data)
        self.assertEqual(result, {"name": "test", "value": 123})
    
    def test_serialize_dict(self):
        """Тест сериализации словаря в YAML"""
        data = {"name": "test", "value": 123}
        result = self.converter.serialize(data)
        self.assertIn('name: test', result)
        self.assertIn('value: 123', result)
    
    def test_validate_valid_yaml(self):
        """Тест валидации корректного YAML"""
        yaml_data = 'name: test\nvalue: 123'
        self.assertTrue(self.converter.validate(yaml_data))


class TestTOMLConverter(unittest.TestCase):
    """Тесты для TOML конвертера"""
    
    def setUp(self):
        self.converter = TOMLConverter()
    
    def test_parse_valid_toml(self):
        """Тест парсинга корректного TOML"""
        toml_data = 'name = "test"\nvalue = 123'
        result = self.converter.parse(toml_data)
        self.assertEqual(result, {"name": "test", "value": 123})
    
    def test_serialize_dict(self):
        """Тест сериализации словаря в TOML"""
        data = {"name": "test", "value": 123}
        result = self.converter.serialize(data)
        self.assertIn('name = "test"', result)
        self.assertIn('value = 123', result)
    
    def test_validate_valid_toml(self):
        """Тест валидации корректного TOML"""
        toml_data = 'name = "test"\nvalue = 123'
        self.assertTrue(self.converter.validate(toml_data))


if __name__ == '__main__':
    unittest.main()
