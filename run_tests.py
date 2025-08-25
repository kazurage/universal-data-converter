#!/usr/bin/env python3
"""
Скрипт для запуска всех тестов универсального конвертера данных
"""
import unittest
import sys
import os

# Добавляем корневую директорию проекта в путь Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_tests():
    """Запускает все тесты"""
    # Обнаруживаем и запускаем все тесты
    loader = unittest.TestLoader()
    test_suite = loader.discover('tests', pattern='test_*.py')
    
    # Запускаем тесты с подробным выводом
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Возвращаем код выхода
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    exit_code = run_tests()
    sys.exit(exit_code)
