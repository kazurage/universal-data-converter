"""
Тесты для Flask приложения
"""
import unittest
import json
import io
from app import app


class TestFlaskApp(unittest.TestCase):
    """Тесты для Flask приложения"""
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_index_page(self):
        """Тест главной страницы"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'\xd0\xa3\xd0\xbd\xd0\xb8\xd0\xb2\xd0\xb5\xd1\x80\xd1\x81\xd0\xb0\xd0\xbb\xd1\x8c\xd0\xbd\xd1\x8b\xd0\xb9 \xd0\xba\xd0\xbe\xd0\xbd\xd0\xb2\xd0\xb5\xd1\x80\xd1\x82\xd0\xb5\xd1\x80', response.data)
    
    def test_api_formats(self):
        """Тест API получения поддерживаемых форматов"""
        response = self.app.get('/api/formats')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('formats', data)
        self.assertIn('json', data['formats'])
        self.assertIn('xml', data['formats'])
    
    def test_api_convert_text_data(self):
        """Тест API конвертации текстовых данных"""
        response = self.app.post('/api/convert', data={
            'source_format': 'json',
            'target_format': 'yaml',
            'text_data': '{"name": "test", "value": 123}'
        })
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('name: test', data['result'])
    
    def test_api_convert_file_upload(self):
        """Тест API конвертации загруженного файла"""
        # Создаем тестовый JSON файл в памяти
        test_json = '{"name": "test", "value": 123}'
        file_data = io.BytesIO(test_json.encode('utf-8'))
        
        response = self.app.post('/api/convert', 
            data={
                'source_format': 'json',
                'target_format': 'yaml',
                'file': (file_data, 'test.json')
            },
            content_type='multipart/form-data'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('name: test', data['result'])
    
    def test_api_convert_auto_detect(self):
        """Тест API конвертации с автоопределением формата"""
        response = self.app.post('/api/convert', data={
            'source_format': 'auto',
            'target_format': 'yaml',
            'text_data': '{"name": "test", "value": 123}'
        })
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['source_format'], 'json')
    
    def test_api_convert_missing_target_format(self):
        """Тест API конвертации без указания целевого формата"""
        response = self.app.post('/api/convert', data={
            'source_format': 'json',
            'text_data': '{"name": "test"}'
        })
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_api_convert_no_data(self):
        """Тест API конвертации без данных"""
        response = self.app.post('/api/convert', data={
            'source_format': 'json',
            'target_format': 'yaml'
        })
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_api_convert_invalid_data(self):
        """Тест API конвертации с некорректными данными"""
        response = self.app.post('/api/convert', data={
            'source_format': 'json',
            'target_format': 'yaml',
            'text_data': '{"name": "test"'  # Некорректный JSON
        })
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_api_validate_valid_data(self):
        """Тест API валидации корректных данных"""
        response = self.app.post('/api/validate', data={
            'format': 'json',
            'text_data': '{"name": "test", "value": 123}'
        })
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['valid'])
        self.assertEqual(data['format'], 'json')
    
    def test_api_validate_invalid_data(self):
        """Тест API валидации некорректных данных"""
        response = self.app.post('/api/validate', data={
            'format': 'json',
            'text_data': '{"name": "test"'  # Некорректный JSON
        })
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertFalse(data['valid'])
    
    def test_api_validate_missing_format(self):
        """Тест API валидации без указания формата"""
        response = self.app.post('/api/validate', data={
            'text_data': '{"name": "test"}'
        })
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_api_download(self):
        """Тест API скачивания файла"""
        response = self.app.post('/api/download',
            json={
                'content': '{"name": "test", "value": 123}',
                'format': 'json',
                'filename': 'test.json'
            }
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')
    
    def test_api_download_missing_data(self):
        """Тест API скачивания без данных"""
        response = self.app.post('/api/download', json={})
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_404_error(self):
        """Тест обработки 404 ошибки"""
        response = self.app.get('/nonexistent')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
