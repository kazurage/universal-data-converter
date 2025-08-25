# Универсальный конвертер форматов данных

Веб-приложение для конвертации между различными форматами данных: JSON, XML, CSV, YAML и TOML.

## 🚀 Возможности

- **Поддерживаемые форматы**: JSON ↔ XML ↔ CSV ↔ YAML ↔ TOML
- **Веб-интерфейс** с современным дизайном и drag & drop загрузкой файлов
- **Автоопределение формата** входных данных
- **Предпросмотр результата** перед скачиванием
- **Валидация данных** для каждого формата
- **Скачивание** конвертированных файлов
- **Обработка ошибок** с понятными сообщениями
- **API endpoints** для программного использования
- **Responsive дизайн** для мобильных устройств

## 📋 Требования

- Python 
- Flask

## 🛠️ Установка

1. **Клонируйте репозиторий**:
```bash
git clone https://github.com/kazurage/universal-data-converter
cd universal-data-converter
```

2. **Создайте виртуальное окружение**:
```bash
python -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate
```

3. **Установите зависимости**:
```bash
pip install -r requirements.txt
```

4. **Запустите приложение**:
```bash
python app.py
```

5. **Откройте браузер** и перейдите по адресу: `http://localhost:5000`

## 🎯 Использование

### Веб-интерфейс

1. Выберите исходный и целевой форматы
2. Загрузите файл (drag & drop) или введите текст
3. Нажмите "Конвертировать"
4. Просмотрите результат и скачайте файл

### API Endpoints

#### Конвертация данных
```http
POST /api/convert
Content-Type: multipart/form-data

source_format: json|xml|csv|yaml|toml|auto
target_format: json|xml|csv|yaml|toml
file: файл для конвертации (опционально)
text_data: текстовые данные (опционально)
```

**Ответ**:
```json
{
  "success": true,
  "result": "конвертированные данные",
  "source_format": "json",
  "target_format": "yaml"
}
```

#### Валидация данных
```http
POST /api/validate
Content-Type: multipart/form-data

format: json|xml|csv|yaml|toml
file: файл для валидации (опционально)
text_data: текстовые данные (опционально)
```

**Ответ**:
```json
{
  "valid": true,
  "format": "json"
}
```

#### Получение поддерживаемых форматов
```http
GET /api/formats
```

**Ответ**:
```json
{
  "formats": ["json", "xml", "csv", "yaml", "yml", "toml"]
}
```

#### Скачивание файла
```http
POST /api/download
Content-Type: application/json

{
  "content": "данные для скачивания",
  "format": "json",
  "filename": "result.json"
}
```

## 📁 Структура проекта

```
universal-data-converter/
├── app.py                 # Основное Flask приложение
├── converters/           # Модули конвертации
│   ├── __init__.py
│   ├── base.py          # Базовый класс конвертера
│   ├── json_converter.py # JSON конвертер
│   ├── xml_converter.py  # XML конвертер
│   ├── csv_converter.py  # CSV конвертер
│   ├── yaml_converter.py # YAML конвертер
│   ├── toml_converter.py # TOML конвертер
│   └── engine.py        # Движок конвертации
├── templates/           # HTML шаблоны
│   ├── base.html
│   ├── index.html
│   ├── 404.html
│   └── 500.html
├── static/             # Статические файлы
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── images/
├── tests/              # Unit тесты
│   ├── __init__.py
│   ├── test_converters.py
│   ├── test_engine.py
│   └── test_app.py
├── requirements.txt    # Зависимости Python
├── Dockerfile         # Docker контейнер
└── README.md          # Документация
```

## 🧪 Тестирование

Запуск всех тестов:
```bash
python -m unittest discover tests
```

Запуск конкретного теста:
```bash
python -m unittest tests.test_converters
python -m unittest tests.test_engine
python -m unittest tests.test_app
```

## 🔧 Конфигурация

### Переменные окружения

- `FLASK_ENV`: `development` или `production`
- `SECRET_KEY`: секретный ключ для Flask сессий
- `MAX_CONTENT_LENGTH`: максимальный размер файла (по умолчанию 10MB)

### Ограничения

- **Максимальный размер файла**: 10MB
- **Поддерживаемые кодировки**: UTF-8
- **Поддерживаемые форматы**: JSON, XML, CSV, YAML, TOML

## 🐳 Docker

Создание Docker образа:
```bash
docker build -t universal-data-converter .
```

Запуск контейнера:
```bash
docker run -p 5000:5000 universal-data-converter
```

## 🤝 Примеры использования

### Конвертация JSON в YAML
```json
// Входные данные (JSON)
{
  "users": [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25}
  ]
}
```

```yaml
# Результат (YAML)
users:
- age: 30
  name: Alice
- age: 25
  name: Bob
```

### Конвертация CSV в JSON
```csv
name,age,city
Alice,30,New York
Bob,25,London
```

```json
[
  {"name": "Alice", "age": 30, "city": "New York"},
  {"name": "Bob", "age": 25, "city": "London"}
]
```

## 📝 Лицензия

Этот проект распространяется под лицензией MIT. См. файл LICENSE для подробностей.

## 🐛 Сообщение об ошибках

Если вы нашли ошибку или у вас есть предложение по улучшению, пожалуйста, создайте issue в репозитории GitHub.

## 👥 Участие в разработке

1. Сделайте fork репозитория
2. Создайте ветку для новой функции (`git checkout -b feature/amazing-feature`)
3. Сделайте commit изменений (`git commit -m 'Add amazing feature'`)
4. Отправьте изменения в ветку (`git push origin feature/amazing-feature`)
5. Создайте Pull Request

## 📊 Статистика

- **Языки программирования**: Python, JavaScript, HTML, CSS
- **Фреймворки**: Flask, Bootstrap 5
- **Библиотеки**: pandas, PyYAML, xmltodict, toml
- **Тесты**: unittest (покрытие > 90%)
- **Совместимость**: Python 3.8+, все современные браузеры
