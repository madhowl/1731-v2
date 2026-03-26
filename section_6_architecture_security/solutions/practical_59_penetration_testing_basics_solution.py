#!/usr/bin/env python3
"""
Практическое занятие 59: Основы пентестинга
Решение упражнений
"""

import socket
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime


# ==============================================================================
# УПРАЖНЕНИЕ 1: Passive Reconnaissance
# ==============================================================================

print("=" * 60)
print("Упражнение 1: Passive Reconnaissance")
print("=" * 60)


class Reconnaissance:
    """Инструменты для разведки"""
    
    @staticmethod
    def get_whois_info(domain: str) -> Dict[str, Any]:
        """Получение информации WHOIS (симуляция)"""
        return {
            'domain': domain,
            'registrar': 'Example Registrar',
            'creation_date': '2020-01-01',
            'expiration_date': '2025-01-01',
            'name_servers': ['ns1.example.com', 'ns2.example.com'],
            'emails': ['admin@example.com']
        }
    
    @staticmethod
    def get_dns_records(domain: str) -> List[Dict[str, str]]:
        """Получение DNS записей (симуляция)"""
        return [
            {'type': 'A', 'value': '93.184.216.34'},
            {'type': 'AAAA', 'value': '::1'},
            {'type': 'MX', 'value': 'mail.example.com'},
            {'type': 'NS', 'value': 'ns1.example.com'},
            {'type': 'TXT', 'value': 'v=spf1 include:_spf.example.com ~all'}
        ]
    
    @staticmethod
    def check_subdomains(domain: str) -> List[Dict[str, str]]:
        """Поиск поддоменов (симуляция)"""
        subdomains = ['www', 'mail', 'ftp', 'admin', 'test', 'dev']
        found = []
        
        for subdomain in subdomains:
            found.append({
                'subdomain': f"{subdomain}.{domain}",
                'ip': '93.184.216.34'
            })
        
        return found
    
    @staticmethod
    def get_http_headers(url: str) -> Dict[str, str]:
        """Получение HTTP заголовков (симуляция)"""
        return {
            'Server': 'nginx/1.18.0',
            'Content-Type': 'text/html; charset=UTF-8',
            'Connection': 'keep-alive',
            'X-Frame-Options': 'SAMEORIGIN',
            'X-Content-Type-Options': 'nosniff'
        }


recon = Reconnaissance()

print("Информация WHOIS:")
whois_info = recon.get_whois_info('example.com')
print(f"  Domain: {whois_info['domain']}")
print(f"  Registrar: {whois_info['registrar']}")

print("\nDNS записи:")
dns_records = recon.get_dns_records('example.com')
for record in dns_records:
    print(f"  {record['type']}: {record['value']}")

print("\nHTTP заголовки:")
headers = recon.get_http_headers('https://example.com')
for key, value in headers.items():
    print(f"  {key}: {value}")


# ==============================================================================
# УПРАЖНЕНИЕ 2: Сканирование портов
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 2: Сканирование портов")
print("=" * 60)


class PortScanner:
    """Сканер портов"""
    
    def __init__(self, timeout: float = 1.0):
        self.timeout = timeout
    
    def scan_port(self, host: str, port: int) -> Dict[str, Any]:
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
    
    def scan_ports(self, host: str, ports: List[int] = None) -> List[Dict[str, Any]]:
        """Сканирование списка портов"""
        if ports is None:
            ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 3306, 3389, 5432, 8080]
        
        results = []
        for port in ports:
            result = self.scan_port(host, port)
            if result['open']:
                results.append(result)
        
        return results
    
    def _get_service_name(self, port: int) -> str:
        """Определение имени сервиса"""
        try:
            return socket.getservbyport(port)
        except:
            return 'unknown'


scanner = PortScanner(timeout=1.0)
print("Сканирование localhost (порт 80 должен быть открыт):")
results = scanner.scan_ports('127.0.0.1', [22, 80, 443, 8080])
for result in results:
    print(f"  Port {result['port']}: {result['service']}")


# ==============================================================================
# УПРАЖНЕНИЕ 3: Сканирование уязвимостей
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 3: Сканирование уязвимостей")
print("=" * 60)


class VulnerabilityScanner:
    """Сканер уязвимостей"""
    
    def __init__(self, target_url: str):
        self.target_url = target_url
    
    def check_security_headers(self) -> Dict[str, Any]:
        """Проверка заголовков безопасности"""
        required_headers = {
            'Strict-Transport-Security': 'HSTS заголовок отсутствует',
            'Content-Security-Policy': 'CSP заголовок отсутствует',
            'X-Content-Type-Options': 'X-Content-Type-Options отсутствует',
            'X-Frame-Options': 'X-Frame-Options отсутствует'
        }
        
        headers = {
            'Server': 'nginx/1.18.0',
            'Content-Type': 'text/html'
        }
        
        results = {}
        for header, message in required_headers.items():
            results[header] = {
                'present': header in headers,
                'value': headers.get(header),
                'warning': message if header not in headers else None
            }
        
        return results
    
    def check_common_vulnerabilities(self) -> List[Dict[str, Any]]:
        """Проверка распространённых уязвимостей"""
        vulnerabilities = []
        
        headers = self.check_security_headers()
        missing_headers = [
            h for h, v in headers.items() 
            if isinstance(v, dict) and not v.get('present', False)
        ]
        
        if missing_headers:
            vulnerabilities.append({
                'type': 'Security Headers',
                'severity': 'medium',
                'description': f'Отсутствуют заголовки: {", ".join(missing_headers)}'
            })
        
        return vulnerabilities


scanner = VulnerabilityScanner('https://example.com')

print("Проверка заголовков безопасности:")
headers_result = scanner.check_security_headers()
for header, result in headers_result.items():
    print(f"  {header}: {'✓' if result['present'] else '✗'}")

print("\nНайденные уязвимости:")
vulns = scanner.check_common_vulnerabilities()
for vuln in vulns:
    print(f"  [{vuln['severity'].upper()}] {vuln['type']}: {vuln['description']}")


# ==============================================================================
# УПРАЖНЕНИЕ 4: Генерация отчёта
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 4: Генерация отчёта")
print("=" * 60)


@dataclass
class Finding:
    """Находка (уязвимость)"""
    title: str
    severity: str
    description: str
    remediation: str
    evidence: List[str] = None
    references: List[str] = None
    cvss: float = 0.0
    
    def __post_init__(self):
        self.evidence = self.evidence or []
        self.references = self.references or []


class PentestReport:
    """Генератор отчёта о пентесте"""
    
    def __init__(self, target: str):
        self.target = target
        self.findings: List[Finding] = []
        self.start_date = datetime.now()
    
    def add_finding(self, finding: Finding):
        """Добавление находки"""
        self.findings.append(finding)
    
    def generate_json(self) -> Dict[str, Any]:
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
    
    def generate_summary(self) -> Dict[str, Any]:
        """Генерация сводки"""
        severity_counts = {}
        for finding in self.findings:
            severity = finding.severity.upper()
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        return {
            'total': len(self.findings),
            'by_severity': severity_counts
        }


report = PentestReport('https://example.com')

report.add_finding(Finding(
    title='Missing Security Headers',
    severity='medium',
    description='Отсутствуют важные заголовки безопасности',
    remediation='Добавить HSTS, CSP, X-Frame-Options заголовки',
    cvss=5.3
))

report.add_finding(Finding(
    title='Outdated TLS Version',
    severity='high',
    description='Используется устаревшая версия TLS',
    remediation='Обновить TLS до версии 1.2 или выше',
    cvss=7.5
))

summary = report.generate_summary()
print(f"Всего находок: {summary['total']}")
print("По критичности:")
for severity, count in summary['by_severity'].items():
    print(f"  {severity}: {count}")


print("\n" + "=" * 60)
print("Все упражнения выполнены!")
print("=" * 60)
