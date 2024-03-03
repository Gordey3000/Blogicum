## Blogicum
### Платформа для блогов. Позволяет вести собственный блог и читать блоги других пользователей.

### Стек:
Python, Django

### Запуск отладочного сервера под windows:
#### В директории с проектом

Создание виртуального окружения:
```
python -m venv venv
```
Активация виртуального окружения:
```
source venv\Scripts\activate
```
Если возникла ошибка 'Имя "source" не распознано' или аналогичная:
```
venv\Scripts\activate
```
Установка зависимостей:
```
pip install -r requirements.txt
```
Запуск отладочного сервера:
```
cd blogicum
python manage.py runserver
```
