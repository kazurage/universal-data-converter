"""
Основное Flask приложение для универсального конвертера данных
"""
from flask import Flask, render_template, request, jsonify, send_file, flash
import os
import io
import tempfile
import logging
from werkzeug.utils import secure_filename
from converters.engine import ConversionEngine, ConversionError

app = Flask(__name__)
app.secret_key = 'universal-data-converter-secret-key'
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB максимум

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Инициализируем движок конвертации
converter_engine = ConversionEngine()

# Поддерживаемые расширения файлов
ALLOWED_EXTENSIONS = {'json', 'xml', 'csv', 'yaml', 'yml', 'toml', 'txt'}

def allowed_file(filename):
    """Проверяет разрешенные расширения файлов"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Главная страница"""
    supported_formats = converter_engine.get_supported_formats()
    return render_template('index.html', formats=supported_formats)

@app.route('/favicon.ico')
def favicon():
    """Favicon"""
    return send_file('static/images/favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/api/convert', methods=['POST'])
def api_convert():
    """API endpoint для конвертации данных"""
    try:
        logger.debug(f"Получен запрос на конвертацию: {request.form}")
        logger.debug(f"Файлы в запросе: {request.files}")
        
        # Получаем параметры
        source_format = request.form.get('source_format', 'auto')
        target_format = request.form.get('target_format')
        
        logger.debug(f"source_format: {source_format}, target_format: {target_format}")
        
        if not target_format:
            logger.error("Целевой формат не указан")
            return jsonify({'error': 'Не указан целевой формат'}), 400
        
        # Получаем данные - либо из файла, либо из текста
        if 'file' in request.files and request.files['file'].filename:
            file = request.files['file']
            logger.debug(f"Получен файл: {file.filename}")
            
            if not allowed_file(file.filename):
                logger.error(f"Неподдерживаемый тип файла: {file.filename}")
                return jsonify({'error': 'Неподдерживаемый тип файла'}), 400
            
            filename = secure_filename(file.filename)
            data = file.stream
            logger.debug(f"Обработка файла: {filename}")
        else:
            text_data = request.form.get('text_data')
            logger.debug(f"Получены текстовые данные: {len(text_data) if text_data else 0} символов")
            
            if not text_data:
                logger.error("Не предоставлены данные для конвертации")
                return jsonify({'error': 'Не предоставлены данные для конвертации'}), 400
            
            data = text_data
            filename = None
        
        # Проверяем размер файла для streaming
        use_streaming = False
        if 'file' in request.files and request.files['file'].filename:
            file_size = request.content_length or 0
            use_streaming = file_size > 5 * 1024 * 1024  # 5MB threshold
        
        # Выполняем конвертацию
        logger.debug(f"Начинаем конвертацию с параметрами: streaming={use_streaming}")
        result = converter_engine.convert(data, source_format, target_format, filename, stream=use_streaming)
        
        # Определяем исходный формат, если нужно
        if source_format == 'auto':
            # Для автоопределения нужно сбросить указатель потока, если это файл
            if hasattr(data, 'seek'):
                data.seek(0)
            detected_format = converter_engine.detect_format(data, filename)
            if hasattr(data, 'seek'):
                data.seek(0)  # Сбрасываем для повторного чтения
        else:
            detected_format = source_format
        logger.debug(f"Конвертация успешна: {detected_format} -> {target_format}")
        
        return jsonify({
            'success': True,
            'result': result,
            'source_format': detected_format,
            'target_format': target_format
        })
        
    except ConversionError as e:
        logger.error(f"Ошибка конвертации: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Внутренняя ошибка сервера: {str(e)}")
        return jsonify({'error': f'Внутренняя ошибка сервера: {str(e)}'}), 500

@app.route('/api/validate', methods=['POST'])
def api_validate():
    """API endpoint для валидации данных"""
    try:
        format_name = request.form.get('format')
        if not format_name:
            return jsonify({'error': 'Не указан формат для валидации'}), 400
        
        # Получаем данные
        if 'file' in request.files and request.files['file'].filename:
            file = request.files['file']
            data = file.stream
        else:
            text_data = request.form.get('text_data')
            if not text_data:
                return jsonify({'error': 'Не предоставлены данные для валидации'}), 400
            data = text_data
        
        # Валидируем
        is_valid = converter_engine.validate_data(data, format_name)
        
        return jsonify({
            'valid': is_valid,
            'format': format_name
        })
        
    except Exception as e:
        return jsonify({'error': f'Ошибка валидации: {str(e)}'}), 500

@app.route('/api/download', methods=['POST'])
def api_download():
    """API endpoint для скачивания конвертированного файла"""
    try:
        logger.debug(f"Download request received: {request.json}")
        
        # Получаем данные из POST запроса
        data = request.json
        if not data or 'content' not in data or 'format' not in data:
            logger.error("Некорректные данные для скачивания")
            return jsonify({'error': 'Некорректные данные для скачивания'}), 400
        
        content = data['content']
        format_name = data['format']
        filename = data.get('filename', f'converted{converter_engine.get_file_extension(format_name)}')
        
        logger.debug(f"Creating file: {filename}, format: {format_name}")
        
        # Создаем временный файл с правильной кодировкой
        temp_file = tempfile.NamedTemporaryFile(
            mode='w', 
            suffix=converter_engine.get_file_extension(format_name), 
            delete=False,
            encoding='utf-8'
        )
        temp_file.write(content)
        temp_file.close()
        
        logger.debug(f"Temporary file created: {temp_file.name}")
        
        # Отправляем файл
        try:
            response = send_file(
                temp_file.name,
                as_attachment=True,
                download_name=filename,
                mimetype=converter_engine.get_mime_type(format_name)
            )
            logger.debug("File sent successfully")
            return response
        finally:
            # Удаляем временный файл после отправки
            try:
                os.unlink(temp_file.name)
                logger.debug(f"Temporary file removed: {temp_file.name}")
            except Exception as e:
                logger.error(f"Error removing temporary file: {e}")
        
    except Exception as e:
        logger.error(f"Ошибка при подготовке файла для скачивания: {str(e)}")
        return jsonify({'error': f'Ошибка при подготовке файла для скачивания: {str(e)}'}), 500

@app.route('/api/formats')
def api_formats():
    """API endpoint для получения списка поддерживаемых форматов"""
    return jsonify({
        'formats': converter_engine.get_supported_formats()
    })

@app.errorhandler(413)
def too_large(e):
    """Обработчик ошибки превышения размера файла"""
    return jsonify({'error': 'Файл слишком большой. Максимальный размер: 10MB'}), 413

@app.errorhandler(404)
def not_found(e):
    """Обработчик ошибки 404"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    """Обработчик ошибки 500"""
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
