import os

os.system('python /webapp/manage.py makemigrations && python /webapp/manage.py migrate')
# os.system("gunicorn --bind=0.0.0.0:8000 --name=webapp webapp.wsgi:application --reload -w 2")
# os.system('python bot.py')
