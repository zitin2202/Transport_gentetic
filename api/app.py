import subprocess

def install_pipenv():
    # Установка pipenv, если не установлен
    try:
        __import__('pipenv')
    except ImportError:
        subprocess.call(['pip', 'install', 'pipenv'])


if __name__ == '__main__':
    print("Проверка зависимостей...")
    install_pipenv()
    subprocess.call(['pipenv', 'install', '--ignore-pipfile'])
    print("Проверка зависимостей завершена")
    import flask_app
    flask_app.application()
