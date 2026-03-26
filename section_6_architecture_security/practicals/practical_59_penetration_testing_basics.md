# Практическое занятие 59: Основы пентестинга

## Методология тестирования на проникновение, сканирование, эксплуатация, отчётность

### Цель занятия:
Изучить основы тестирования на проникновение, освоить методологию и инструменты пентестинга, научиться выявлять уязвимости.

### Задачи:
1. Понять методологию пентестинга
2. Освоить инструменты сканирования
3. Научиться выявлять уязвимости
4. Составить отчёт о найденных уязвимостях

### План работы:
1. Введение в пентестинг
2. Методология
3. Инструменты
4. Типичные уязвимости
5. Отчётность
6. Практические задания

---

## 1. Введение в пентестинг

Тестирование на проникновение (pentesting) - это симуляция атаки на систему для выявления уязвимостей.

### Типы пентестинга:

- **Black Box** - без информации о системе
- **White Box** - с полной информацией
- **Gray Box** - частичная информация

### Этапы пентестинга:

1. Разведка (Reconnaissance)
2. Сканирование (Scanning)
3. Получение доступа (Exploitation)
4. Поддержание доступа (Maintaining Access)
5. Анализ и отчётность

---

## 2. Разведка

### Пример 1: Passive Reconnaissance

```python
import socket
import whois
import requests
from urllib.parse import urlparse

class Reconnaissance:
    """Инструменты для разведки"""
    
    @staticmethod
    def get_whois_info(domain: str) -> dict:
        """Получение информации WHOIS"""
        try:
            w = whois.whois(domain)
            return {
                'registrar': w.registrar,
                'creation_date': w.creation_date,
                'expiration_date': w.expiration_date,
                'name_servers': w.name_servers,
                'emails': w.emails
            }
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def get_dns_records(domain: str) -> list:
        """Получение DNS записей"""
        import dns.resolver
        
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME']
        results = []
        
        for record_type in record_types:
            try:
                answers = dns.resolver.resolve(domain, record_type)
                for rdata in answers:
                    results.append({
                        'type': record_type,
                        'value': str(rdata)
                    })
            except:
                pass
        
        return results
    
    @staticmethod
    def check_subdomains(domain: str) -> list:
        """Поиск поддоменов"""
        subdomains = ['www', 'mail', 'ftp', 'admin', 'test', 'dev']
        found = []
        
        for subdomain in subdomains:
            try:
                full_domain = f"{subdomain}.{domain}"
                ip = socket.gethostbyname(full_domain)
                found.append({
                    'subdomain': full_domain,
                    'ip': ip
                })
            except:
                pass
        
        return found
    
    @staticmethod
    def get_http_headers(url: str) -> dict:
        """Получение HTTP заголовков"""
        try:
            response = requests.head(url, timeout=5)
            return dict(response.headers)
        except Exception as e:
            return {'error': str(e)}

# Использование
recon = Reconnaissance()

# Информация WHOIS
whois_info = recon.get_whois_info('example.com')
print(f"WHOIS: {whois_info}")

# DNS записи
dns_records = recon.get_dns_records('example.com')
print(f"DNS: {dns_records}")

# HTTP заголовки
headers = recon.get_http_headers('https://example.com')
print(f"Headers: {headers}")
```

---

## 3. Сканирование

### Пример 2: Сканирование портов

```python
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

class PortScanner:
    """Сканер портов"""
    
    def __init__(self, timeout: float = 1.0):
        self.timeout = timeout
    
    def scan_port(self, host: str, port: int) -> dict:
        """Сканирование одного порта"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            
            return {
                'port': port,
                'open': result == 0,
                'service': self._get_service_name(port)
            }
        except:
            return {'port': port, 'open': False}
    
    def scan_ports(self, host: str, ports: list = None) -> list:
        """Сканирование списка портов"""
        if ports is None:
            ports = list(range(1, 1025))
        
        results = []
        
        with ThreadPoolExecutor(max_workers=100) as executor:
            futures = {
                executor.submit(self.scan_port, host, port): port
                for port in ports
            }
            
            for future in as_completed(futures):
                result = future.result()
                if result['open']:
                    results.append(result)
        
        return results
    
    def _get_service_name(self, port: int) -> str:
        """Определение имени сервиса"""
        try:
            return socket.getservbyport(port)
        except:
            return 'unknown'

# Использование
scanner = PortScanner(timeout=1.0)
results = scanner.scan_ports('scanme.nmap.org', [22, 80, 443, 8080])
print(f"Open ports: {results}")
```

### Пример 3: Сканирование уязвимостей

```python
import requests
from urllib.parse import urljoin

class VulnerabilityScanner:
    """Сканер уязвимостей"""
    
    def __init__(self, target_url: str):
        self.target_url = target_url
        self.session = requests.Session()
    
    def check_ssl(self) -> dict:
        """Проверка SSL сертификата"""
        import ssl
        import socket
        
        hostname = urlparse(self.target_url).netloc.split(':')[0]
        
        try:
            context = ssl.create_default_context()
            with socket.create_connection((hostname, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    return {
                        'valid': True,
                        'issuer': cert.get('issuer'),
                        'version': cert.get('version'),
                        'subject': cert.get('subject')
                    }
        except Exception as e:
            return {'valid': False, 'error': str(e)}
    
    def check_security_headers(self) -> dict:
        """Проверка заголовков безопасности"""
        required_headers = {
            'Strict-Transport-Security': 'HSTS заголовок отсутствует',
            'Content-Security-Policy': 'CSP заголовок отсутствует',
            'X-Content-Type-Options': 'X-Content-Type-Options отсутствует',
            'X-Frame-Options': 'X-Frame-Options отсутствует'
        }
        
        try:
            response = self.session.head(self.target_url)
            headers = dict(response.headers)
            
            results = {}
            for header, message in required_headers.items():
                results[header] = {
                    'present': header in headers,
                    'value': headers.get(header),
                    'warning': message if header not in headers else None
                }
            
            return results
        except Exception as e:
            return {'error': str(e)}
    
    def check_common_vulnerabilities(self) -> list:
        """Проверка распространённых уязвимостей"""
        vulnerabilities = []
        
        # Проверка на SSL
        ssl_result = self.check_ssl()
        if not ssl_result.get('valid', True):
            vulnerabilities.append({
                'type': 'SSL/TLS',
                'severity': 'high',
                'description': 'Проблемы с SSL сертификатом'
            })
        
        # Проверка заголовков
        headers_result = self.check_security_headers()
        missing_headers = [
            h for h, v in headers_result.items() 
            if isinstance(v, dict) and not v.get('present', False)
        ]
        if missing_headers:
            vulnerabilities.append({
                'type': 'Security Headers',
                'severity': 'medium',
                'description': f'Отсутствуют заголовки: {", ".join(missing_headers)}'
            })
        
        return vulnerabilities

# Использование
scanner = VulnerabilityScanner('https://example.com')

# Проверка SSL
ssl_result = scanner.check_ssl()
print(f"SSL: {ssl_result}")

# Проверка заголовков
headers_result = scanner.check_security_headers()
print(f"Headers: {headers_result}")

# Уязвимости
vulns = scanner.check_common_vulnerabilities()
print(f"Vulnerabilities: {vulns}")
```

---

## 4. Типичные уязвимости

### Пример 4: Проверка на SQL Injection

```python
import requests
from urllib.parse import urljoin

class SQLInjectionScanner:
    """Сканер SQL инъекций"""
    
    def __init__(self):
        self.payloads = [
            "' OR '1'='1",
            "' OR '1'='1' --",
            "' OR '1'='1' /*",
            "admin' --",
            "admin' #",
            "' UNION SELECT NULL--",
            "1' AND '1'='1",
            "1' AND '1'='2",
            "1' ORDER BY 1--",
            "1' ORDER BY 10--"
        ]
    
    def scan(self, url: str, params: dict = None) -> list:
        """Сканирование на SQL инъекции"""
        vulnerabilities = []
        
        if params:
            for param_name in params.keys():
                for payload in self.payloads:
                    test_params = params.copy()
                    test_params[param_name] = payload
                    
                    try:
                        response = requests.get(url, params=test_params, timeout=5)
                        
                        # Проверка индикаторов ошибок
                        if self._check_error(response.text):
                            vulnerabilities.append({
                                'url': url,
                                'parameter': param_name,
                                'payload': payload,
                                'type': 'SQL Injection',
                                'severity': 'high'
                            })
                            break
                    
                    except:
                        pass
        
        return vulnerabilities
    
    def _check_error(self, text: str) -> bool:
        """Проверка текста на наличие ошибок БД"""
        error_keywords = [
            'mysql_fetch',
            'mysql_num_rows',
            'ORA-',
            'Microsoft SQL',
            'PostgreSQL',
            'SQLite/JDBCDriver',
            'error in your SQL'
        ]
        
        text_lower = text.lower()
        return any(keyword.lower() in text_lower for keyword in error_keywords)

# Использование
scanner = SQLInjectionScanner()
# vulnerabilities = scanner.scan('http://example.com/search.php', {'query': 'test'})
```

---

## 5. Отчётность

### Пример 5: Генерация отчёта

```python
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict
import json

@dataclass
class Finding:
    """Находка (уязвимость)"""
    title: str
    severity: str
    description: str
    remediation: str
    evidence: List[str] = field(default_factory=list)
    references: List[str] = field(default_factory=list)
    cvss: float = 0.0

class PentestReport:
    """Генератор отчёта о пентесте"""
    
    def __init__(self, target: str):
        self.target = target
        self.findings: List[Finding] = []
        self.start_date = datetime.now()
    
    def add_finding(self, finding: Finding):
        """Добавление находки"""
        self.findings.append(finding)
    
    def generate_json(self) -> dict:
        """Генерация JSON отчёта"""
        return {
            'report': {
                'target': self.target,
                'date': self.start_date.isoformat(),
                'findings_count': len(self.findings),
                'findings': [
                    {
                        'title': f.title,
                        'severity': f.severity,
                        'cvss': f.cvss,
                        'description': f.description,
                        'remediation': f.remediation,
                        'evidence': f.evidence,
                        'references': f.references
                    }
                    for f in self.findings
                ]
            }
        }
    
    def generate_html(self) -> str:
        """Генерация HTML отчёта"""
        html = f"""
        <html>
        <head>
            <title>Pentest Report - {self.target}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .finding {{ border: 1px solid #ddd; padding: 15px; margin: 10px 0; }}
                .critical {{ border-left: 5px solid #d9534f; }}
                .high {{ border-left: 5px solid #f0ad4e; }}
                .medium {{ border-left: 5px solid #5bc0de; }}
                .low {{ border-left: 5px solid #5cb85c; }}
                .severity {{ font-weight: bold; }}
            </style>
        </head>
        <body>
            <h1>Pentest Report</h1>
            <p><strong>Target:</strong> {self.target}</p>
            <p><strong>Date:</strong> {self.start_date.strftime('%Y-%m-%d')}</p>
            <p><strong>Findings:</strong> {len(self.findings)}</p>
        """
        
        for finding in self.findings:
            html += f"""
            <div class="finding {finding.severity}">
                <h2>{finding.title}</h2>
                <p><span class="severity">{finding.severity.upper()}</span> | CVSS: {finding.cvss}</p>
                <p>{finding.description}</p>
                <h3>Remediation</h3>
                <p>{finding.remediation}</p>
            </div>
            """
        
        html += "</body></html>"
        return html

# Использование
report = PentestReport('https://example.com')

# Добавление находок
report.add_finding(Finding(
    title='Missing Security Headers',
    severity='medium',
    description='Отсутствуют важные заголовки безопасности',
    remediation='Добавить HSTS, CSP, X-Frame-Options заголовки',
    cvss=5.3
))

# Генерация отчёта
json_report = report.generate_json()
html_report = report.generate_html()

print(json.dumps(json_report, indent=2))
```

---

## 6. Практические задания

### Задание 1: Разведка

Проведите пассивную разведку:
- WHOIS информация
- DNS записи
- HTTP заголовки
- Поддомены

### Задание 2: Сканирование

Сканируйте целевой хост:
- Определение открытых портов
- Определение сервисов
- Определение версий

### Задание 3: Проверка уязвимостей

Проверьте веб-приложение:
- SSL/TLS
- Заголовки безопасности
- SQL инъекции
- XSS

### Задание 4: Анализ

Проанализируйте результаты:
- Определение критичности
- Рекомендации по исправлению
- CVSS оценка

### Задание 5: Отчёт

Составьте отчёт:
- Структура отчёта
- Описание уязвимостей
- Рекомендации
- Приоритизация

---

## Контрольные вопросы:

1. Какие этапы пентестинга вы знаете?
2. В чём разница между black box и white box тестированием?
3. Какие инструменты для сканирования портов вы знаете?
4. Что такое CVSS?
5. Как составлять отчёт о пентесте?
