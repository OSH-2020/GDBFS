import os


os.system("python3 manage.py migrate")
print("please open \033[1;31;48mhttp://localhost:8000/home\033[0m in browser")
os.system("python3 manage.py runserver 0.0.0.0:8000")