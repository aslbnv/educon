# О проекте
Целью проекта являлась разработка системы управления обучением. Основной функционал системы:

 - Создание учебных курсов
 - Наполнение курсов контентом
 - Распределение курсов по пользователям
 - Возможность пройти курс

# Запуск
Помимо основной команды runserver, используется команда для запуска фоновых задач:
```python
python manage.py process_tasks
python manage.py runserver
```
