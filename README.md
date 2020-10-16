# упрощенная версия бота 

## Для запуска требуется
- для первого запуска проекта `docker-compose up --build -d`
- для последующих запусков `docker-compose up -d`
- `pip install -r requirements.txt`
- `./webapp/manage.py makemigrations && ./webapp/manage.py migrate`
- для запуска админки `cd webapp && ./manamge.py runserver`
- для запуска бота `cd bot && python bot.py`
