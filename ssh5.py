import paramiko

# Замените следующие переменные на ваши данные
hostname = '94.228.123.59'
username = 'root'
password = 'p9xiwE5t@HPt^B'

# Подключение к серверу
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh.connect(hostname, username=username, password=password)
    print("Подключено к серверу")
    
    # Получение информации о системе
    stdin, stdout, stderr = ssh.exec_command('uptime | awk -F ", " \'{print $1}\'')
    uptime = stdout.read().decode().strip()
    print("Загрузка системы:", uptime)

    stdin, stdout, stderr = ssh.exec_command('df -h / | awk \'{print $5, "от", $2}\'')
    disk_usage = stdout.read().decode().strip()
    print("Использование /:", disk_usage)

    stdin, stdout, stderr = ssh.exec_command('free -m | awk \'/Mem:/ {print $3/$2 * 100.0}\'')
    memory_usage = stdout.read().decode().strip()
    print("Использование памяти:", memory_usage + "%")

except paramiko.AuthenticationException:
    print("Не удалось подключиться. Неверное имя пользователя или пароль.")
except paramiko.SSHException as e:
    print("Ошибка SSH:", str(e))
finally:
    ssh.close()
    print("Отключено от сервера")