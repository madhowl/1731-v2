# Практическое занятие 61: Безопасность сетевого программирования

## TLS/SSL, безопасные соединения, валидация сертификатов, защита от атак

### Цель занятия:
Изучить основы безопасности сетевого программирования, освоить TLS/SSL, научиться создавать защищённые сетевые приложения.

### Задачи:
1. Понять основы сетевой безопасности
2. Освоить TLS/SSL
3. Научиться валидировать сертификаты
4. Защититься от сетевых атак

### План работы:
1. Основы сетевой безопасности
2. TLS/SSL
3. Валидация сертификатов
4. Защищённые соединения
5. Практические задания

---

## 1. Основы сетевой безопасности

### Пример 1: Безопасный HTTP клиент

```python
import requests
from urllib.parse import urlparse

class SecureHTTPClient:
    """Безопасный HTTP клиент"""
    
    def __init__(self, verify_ssl: bool = True, cert_path: str = None):
        self.session = requests.Session()
        self.session.verify = verify_ssl
        
        if cert_path:
            self.session.cert = cert_path
    
    def get(self, url: str, **kwargs) -> requests.Response:
        """Безопасный GET запрос"""
        return self.session.get(url, **kwargs)
    
    def post(self, url: str, **kwargs) -> requests.Response:
        """Безопасный POST запрос"""
        return self.session.post(url, **kwargs)

# Использование
client = SecureHTTPClient(verify_ssl=True)
# response = client.get('https://example.com')
```

### Пример 2: TLS соединение

```python
import ssl
import socket

class TLSServer:
    """TLS сервер"""
    
    def __init__(self, cert_file: str, key_file: str):
        self.cert_file = cert_file
        self.key_file = key_file
    
    def create_context(self) -> ssl.SSLContext:
        """Создание SSL контекста"""
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(self.cert_file, self.key_file)
        
        # Настройка безопасных параметров
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        context.set_ciphers('ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM')
        
        return context

# Использование
# context = TLSServer('server.crt', 'server.key').create_context()
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
#     sock.bind(('0.0.0.0', 8443))
#     with context.wrap_socket(sock, server_side=True) as ssock:
#         # обработка соединений
```

---

## 2. Защита от атак

### Пример 3: Защита от SSRF

```python
import ipaddress
from urllib.parse import urlparse

class SSRFProtection:
    """Защита от SSRF атак"""
    
    # Заблокированные IP диапазоны
    BLOCKED_RANGES = [
        ipaddress.ip_network('10.0.0.0/8'),
        ipaddress.ip_network('172.16.0.0/12'),
        ipaddress.ip_network('192.168.0.0/16'),
        ipaddress.ip_network('127.0.0.0/8'),
        ipaddress.ip_network('169.254.0.0/16'),
        ipaddress.ip_network('0.0.0.0/8'),
    ]
    
    BLOCKED_HOSTS = [
        'localhost',
        'metadata.google.internal',
        '169.254.169.254',
    ]
    
    @classmethod
    def is_allowed_url(cls, url: str) -> bool:
        """Проверка URL на SSRF"""
        try:
            parsed = urlparse(url)
            hostname = parsed.hostname
            
            if not hostname:
                return False
            
            # Проверка на blocked hosts
            if hostname.lower() in cls.BLOCKED_HOSTS:
                return False
            
            # Разрешение DNS
            try:
                ip = socket.gethostbyname(hostname)
            except socket.gaierror:
                return True
            
            # Проверка IP
            ip_obj = ipaddress.ip_address(ip)
            
            for blocked_range in cls.BLOCKED_RANGES:
                if ip_obj in blocked_range:
                    return False
            
            return True
        
        except Exception:
            return False

# Использование
urls_to_check = [
    'http://example.com',
    'http://169.254.169.254/latest/meta-data',
    'http://localhost/admin',
]

for url in urls_to_check:
    allowed = SSRFProtection.is_allowed_url(url)
    print(f"{url}: {'allowed' if allowed else 'blocked'}")
```

---

## 3. Практические задания

### Задание 1: TLS клиент

Создайте безопасный TLS клиент с валидацией сертификатов.

### Задание 2: TLS сервер

Создайте TLS сервер с безопасной конфигурацией.

### Задание 3: Защита от SSRF

Реализуйте защиту от SSRF атак.

### Задание 4: Rate limiting

Создайте систему ограничения частоты запросов.

### Задание 5: Защита от DDoS

Реализуйте базовую защиту от DDoS атак.
