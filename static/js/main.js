// Основной JavaScript для универсального конвертера данных

// Глобальные переменные
let currentResult = null;
let currentFormat = null;
let currentFilename = null;

// Инициализация Drop Zone
function initializeDropZone() {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const fileInfo = document.getElementById('fileInfo');
    const fileName = document.getElementById('fileName');
    const fileSize = document.getElementById('fileSize');

    // Обработчики drag & drop
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileSelect(files[0]);
        }
    });

    // Клик по drop zone
    dropZone.addEventListener('click', () => {
        fileInput.click();
    });

    // Выбор файла через input
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileSelect(e.target.files[0]);
        }
    });

    function handleFileSelect(file) {
        // Проверка размера файла (10MB)
        if (file.size > 10 * 1024 * 1024) {
            showAlert('Файл слишком большой. Максимальный размер: 10MB', 'danger');
            return;
        }

        // Проверка типа файла
        const allowedTypes = ['json', 'xml', 'csv', 'yaml', 'yml', 'toml', 'txt'];
        const fileExtension = file.name.split('.').pop().toLowerCase();
        
        if (!allowedTypes.includes(fileExtension)) {
            showAlert('Неподдерживаемый тип файла', 'danger');
            return;
        }

        // Устанавливаем файл в input
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        fileInput.files = dataTransfer.files;

        // Показываем информацию о файле
        fileName.textContent = file.name;
        fileSize.textContent = formatFileSize(file.size);
        fileInfo.style.display = 'block';
        
        // Сохраняем имя файла для автоопределения формата
        currentFilename = file.name;
        
        // Автоматически устанавливаем исходный формат, если возможно
        if (allowedTypes.includes(fileExtension) && fileExtension !== 'txt') {
            document.getElementById('sourceFormat').value = fileExtension;
        }
        
        // Очищаем результат при выборе нового файла
        hideResult();
    }
}

// Инициализация формы
function initializeForm() {
    const form = document.getElementById('convertForm');
    const validateBtn = document.getElementById('validateBtn');
    
    form.addEventListener('submit', handleConvert);
    validateBtn.addEventListener('click', handleValidate);
    
    // Переключение между вкладками
    const tabs = document.querySelectorAll('#inputTabs button');
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Очищаем результат при смене вкладки
            hideResult();
        });
    });
    
    // Отслеживание изменений в текстовом поле
    const textInput = document.getElementById('textInput');
    textInput.addEventListener('input', () => {
        hideResult();
    });
}

// Инициализация обработчиков результата
function initializeResultHandlers() {
    const copyBtn = document.getElementById('copyBtn');
    const downloadBtn = document.getElementById('downloadBtn');
    const wrapTextCheckbox = document.getElementById('wrapText');
    
    copyBtn.addEventListener('click', copyResult);
    downloadBtn.addEventListener('click', downloadResult);
    wrapTextCheckbox.addEventListener('change', toggleTextWrap);
}

// Обработка конвертации
async function handleConvert(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const targetFormat = formData.get('target_format');
    
    if (!targetFormat) {
        showAlert('Выберите целевой формат', 'warning');
        return;
    }
    
            // Проверяем, что есть данные для конвертации
        const fileInput = document.getElementById('fileInput');
        const hasFile = fileInput.files.length > 0 && fileInput.files[0].size > 0;
        const hasText = formData.get('text_data') && formData.get('text_data').trim();
        
        // Проверяем активную вкладку
        const activeTab = document.querySelector('#inputTabs .nav-link.active').id;
        
        console.log('Debug - hasFile:', hasFile, 'files count:', fileInput.files.length);
        console.log('Debug - hasText:', hasText, 'text length:', formData.get('text_data') ? formData.get('text_data').length : 0);
        console.log('Debug - activeTab:', activeTab);
    
    if (activeTab === 'file-tab' && !hasFile) {
        showAlert('Загрузите файл для конвертации', 'warning');
        return;
    }
    
    if (activeTab === 'text-tab' && !hasText) {
        showAlert('Введите текст для конвертации', 'warning');
        return;
    }
    
    if (!hasFile && !hasText) {
        showAlert('Загрузите файл или введите текст для конвертации', 'warning');
        return;
    }
    
    showLoading(true);
    
    try {
        const response = await fetch('/api/convert', {
            method: 'POST',
            body: formData
        });
        
        console.log('Response status:', response.status);
        
        const result = await response.json();
        console.log('Conversion result:', result);
        
        if (response.ok && result.success) {
            showResult(result);
            showAlert('Конвертация выполнена успешно!', 'success');
        } else {
            showAlert(result.error || 'Ошибка конвертации', 'danger');
        }
    } catch (error) {
        showAlert('Ошибка соединения с сервером', 'danger');
        console.error('Conversion error:', error);
    } finally {
        console.log('Hiding loading modal in finally block');
        showLoading(false);
    }
}

// Обработка валидации
async function handleValidate() {
    const activeTab = document.querySelector('#inputTabs .nav-link.active').id;
    const formData = new FormData();
    
    // Определяем формат для валидации
    const sourceFormat = document.getElementById('sourceFormat').value;
    if (sourceFormat === 'auto') {
        showAlert('Выберите конкретный формат для валидации', 'warning');
        return;
    }
    
    formData.append('format', sourceFormat);
    
    // Получаем данные в зависимости от активной вкладки
    if (activeTab === 'file-tab') {
        const fileInput = document.getElementById('fileInput');
        if (!fileInput.files[0] || fileInput.files[0].size === 0) {
            showAlert('Выберите файл для валидации', 'warning');
            return;
        }
        formData.append('file', fileInput.files[0]);
    } else {
        const textData = document.getElementById('textInput').value.trim();
        if (!textData) {
            showAlert('Введите текст для валидации', 'warning');
            return;
        }
        formData.append('text_data', textData);
    }
    
    showLoading(true);
    
    try {
        const response = await fetch('/api/validate', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.valid) {
            showAlert(`Данные корректны для формата ${result.format.toUpperCase()}`, 'success');
        } else {
            showAlert(`Данные не соответствуют формату ${result.format.toUpperCase()}`, 'danger');
        }
    } catch (error) {
        showAlert('Ошибка валидации', 'danger');
        console.error('Validation error:', error);
    } finally {
        console.log('Hiding loading modal in validation finally block');
        showLoading(false);
    }
}

// Показ результата
function showResult(result) {
    console.log('Showing result:', result);
    
    currentResult = result.result;
    currentFormat = result.target_format;
    
    const resultSection = document.getElementById('resultSection');
    const resultContent = document.getElementById('resultContent');
    const conversionInfo = document.getElementById('conversionInfo');
    
    console.log('Result elements:', {resultSection, resultContent, conversionInfo});
    
    resultContent.textContent = result.result;
    conversionInfo.textContent = `${result.source_format.toUpperCase()} → ${result.target_format.toUpperCase()}`;
    
    resultSection.style.display = 'block';
    resultSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    resultSection.classList.add('fade-in');
    
    console.log('Result displayed successfully');
}

// Скрытие результата
function hideResult() {
    const resultSection = document.getElementById('resultSection');
    resultSection.style.display = 'none';
    currentResult = null;
    currentFormat = null;
}

// Копирование результата
async function copyResult() {
    if (!currentResult) return;
    
    try {
        await navigator.clipboard.writeText(currentResult);
        showAlert('Результат скопирован в буфер обмена', 'success');
    } catch (error) {
        // Fallback для старых браузеров
        const textArea = document.createElement('textarea');
        textArea.value = currentResult;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        showAlert('Результат скопирован в буфер обмена', 'success');
    }
}

// Скачивание результата
async function downloadResult() {
    if (!currentResult || !currentFormat) {
        console.error('No result or format available for download');
        return;
    }
    
    console.log('Starting download:', {format: currentFormat, contentLength: currentResult.length});
    
    try {
        const downloadData = {
            content: currentResult,
            format: currentFormat,
            filename: generateFilename()
        };
        
        console.log('Download data:', downloadData);
        
        const response = await fetch('/api/download', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(downloadData)
        });
        
        console.log('Download response status:', response.status);
        
        if (response.ok) {
            const blob = await response.blob();
            console.log('Blob created, size:', blob.size);
            
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = generateFilename();
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            showAlert('Файл загружен', 'success');
            console.log('Download completed successfully');
        } else {
            const errorText = await response.text();
            console.error('Download failed:', response.status, errorText);
            showAlert(`Ошибка при скачивании файла: ${response.status}`, 'danger');
        }
    } catch (error) {
        showAlert('Ошибка при скачивании файла', 'danger');
        console.error('Download error:', error);
    }
}

// Переключение переноса строк
function toggleTextWrap() {
    const resultContent = document.getElementById('resultContent');
    const wrapText = document.getElementById('wrapText');
    
    if (wrapText.checked) {
        resultContent.classList.add('wrap-text');
    } else {
        resultContent.classList.remove('wrap-text');
    }
}

// Показ индикатора загрузки
let loadingModal = null;

function showLoading(show) {
    const modalElement = document.getElementById('loadingModal');
    
    if (show) {
        if (!loadingModal) {
            loadingModal = new bootstrap.Modal(modalElement, {
                backdrop: 'static',
                keyboard: false
            });
        }
        loadingModal.show();
        console.log('Loading modal shown');
    } else {
        if (loadingModal) {
            loadingModal.hide();
            console.log('Loading modal hidden');
        }
        // Дополнительная очистка - убираем backdrop вручную
        setTimeout(() => {
            // Убираем все модальные элементы
            const backdrop = document.querySelector('.modal-backdrop');
            if (backdrop) {
                backdrop.remove();
            }
            
            // Скрываем само модальное окно
            modalElement.style.display = 'none';
            modalElement.classList.remove('show');
            modalElement.setAttribute('aria-hidden', 'true');
            modalElement.removeAttribute('aria-modal');
            
            // Восстанавливаем body
            document.body.classList.remove('modal-open');
            document.body.style.overflow = '';
            document.body.style.paddingRight = '';
            
            console.log('Manual modal cleanup completed');
        }, 300);
    }
}

// Показ уведомлений
function showAlert(message, type = 'info') {
    const alertContainer = document.createElement('div');
    alertContainer.className = `alert alert-${type} alert-dismissible fade show`;
    alertContainer.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const main = document.querySelector('main');
    main.insertBefore(alertContainer, main.firstChild);
    
    // Автоматически скрываем через 5 секунд
    setTimeout(() => {
        if (alertContainer.parentNode) {
            alertContainer.remove();
        }
    }, 5000);
}

// Форматирование размера файла
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Генерация имени файла для скачивания
function generateFilename() {
    const timestamp = new Date().toISOString().slice(0, 19).replace(/:/g, '-');
    const extension = getFileExtension(currentFormat);
    
    if (currentFilename) {
        const baseName = currentFilename.split('.')[0];
        return `${baseName}_converted_${timestamp}${extension}`;
    }
    
    return `converted_${timestamp}${extension}`;
}

// Получение расширения файла по формату
function getFileExtension(format) {
    const extensions = {
        'json': '.json',
        'xml': '.xml',
        'csv': '.csv',
        'yaml': '.yaml',
        'yml': '.yml',
        'toml': '.toml'
    };
    return extensions[format] || '.txt';
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    initializeDropZone();
    initializeForm();
    initializeResultHandlers();
});
