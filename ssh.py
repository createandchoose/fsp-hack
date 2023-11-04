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

host = '94.228.123.59'
port = 22
username = 'root'
password = 'hicU?BnqfUAy64'

if ssh_connect(host, port, username, password):
    print("Подключение успешно установлено!")
else:
    print("Не удалось установить подключение.")