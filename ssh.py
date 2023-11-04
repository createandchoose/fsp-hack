import paramiko

def ssh_connect(host, port, username, password):
    try:
        client = paramiko.SSHClient()

        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        client.connect(hostname=host, port=port, username=username, password=password)

        return True
    except Exception as e:
        print(f"Ошибка подключения: {e}")
        return False
    finally:
        client.close()

host = 'ваш_ip_адрес_сервера'
port = 22  # порт SSH
username = 'ваше_имя_пользователя'
password = 'ваш_пароль'

if ssh_connect(host, port, username, password):
    print("Подключение успешно установлено!")
else:
    print("Не удалось установить подключение.")