# Название проекта
HR Assistant

# Описание
Это веб-приложение на **Streamlit**, которое использует OpenAI API для обработки запросов.  

## Установка и запуск
Скачайте и разархивируйте HR_Assistant.zip
Запустите коммандную строку и перейдите в папку
cd your/path/to/folder/HR_Assistant

### 1. Установите Python 3.11
Если у вас не установлен Python версии 3.11, скачайте и установите его с официального сайта 
(https://www.python.org/downloads/release/python-3110/)
Проверить текущую версию можно командой:
python --version

### 2. Создайте и активируйте виртуальную среду
python -m venv venv
source venv/bin/activate   # для Linux/MacOS
venv\Scripts\activate      # для Windows

### 3. Установите зависимости
pip install -r requirements.txt

### 4. Настройте переменные окружения
Создайте файл .env в корне проекта и добавьте в него ваш OpenAI API ключ:
OPENAI_API_KEY=ваш_ключ

### 5. Запустите приложение
streamlit run streamlit_frontend.py


