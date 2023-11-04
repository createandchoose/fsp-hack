import paramiko

def ssh_connect(host, port, username, password):
    try:
        # Создаем объект SSHClient
        client = paramiko.SSHClient()

        # Устанавливаем политику подтверждения хоста (можно добавить варианты для других политик)
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Подключаемся к серверу
        client.connect(hostname=host, port=port, username=username, password=password)

        # Если подключение установлено успешно, возвращаем True
        return True
    except Exception as e:
        # Если произошла ошибка при подключении, выводим ошибку и возвращаем False
        print(f"Ошибка подключения: {e}")
        return False
    finally:
        # Всегда закрываем соединение, когда оно больше не нужно
        client.close()

# Задаем параметры подключения к серверу
host = 'ваш_ip_адрес_сервера'
port = 22  # порт SSH
username = 'ваше_имя_пользователя'
password = 'ваш_пароль'

# Вызываем функцию для подключения
if ssh_connect(host, port, username, password):
    print("Подключение успешно установлено!")
else:
    print("Не удалось установить подключение.")