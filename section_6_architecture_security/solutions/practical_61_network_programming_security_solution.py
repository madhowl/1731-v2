#!/usr/bin/env python3
"""
Практическое занятие 61: Сетевое программирование и безопасность
Решение упражнений
"""

import socket
import ssl
import hashlib
import hmac
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime


# ==============================================================================
# УПРАЖНЕНИЕ 1: Secure Socket Server
# ==============================================================================

print("=" * 60)
print("Упражнение 1: Secure Socket Server")
print("=" * 60)


class SecureSocketServer:
    """Защищённый сервер на сокетах"""
    
    def __init__(self, host: str = '0.0.0.0', port: int = 8443, 
                 cert_file: str = 'server.crt', key_file: str = 'server.key'):
        self.host = host
        self.port = port
        self.cert_file = cert_file
        self.key_file = key_file
        self.socket = None
    
    def create_ssl_context(self) -> ssl.SSLContext:
        """Создание SSL контекста"""
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(self.cert_file, self.key_file)
        
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        context.set_ciphers('ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM:DHE+CHACHA20')
        
        return context
    
    def start(self) -> bool:
        """Запуск сервера"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            
            print(f"Server listening on {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"Error starting server: {e}")
            return False
    
    def stop(self):
        """Остановка сервера"""
        if self.socket:
            self.socket.close()


server = SecureSocketServer()
print("Server created")
print(f"Host: {server.host}, Port: {server.port}")


# ==============================================================================
# УПРАЖНЕНИЕ 2: Secure Client
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 2: Secure Client")
print("=" * 60)


class SecureSocketClient:
    """Защищённый клиент на сокетах"""
    
    def __init__(self, host: str, port: int, ca_file: str = 'ca.crt'):
        self.host = host
        self.port = port
        self.ca_file = ca_file
        self.socket = None
        self.ssl_socket = None
    
    def create_ssl_context(self) -> ssl.SSLContext:
        """Создание SSL контекста для клиента"""
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.load_verify_locations(self.ca_file)
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED
        
        return context
    
    def connect(self) -> bool:
        """Подключение к серверу"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            context = self.create_ssl_context()
            self.ssl_socket = context.wrap_socket(
                self.socket, 
                server_hostname=self.host
            )
            self.ssl_socket.connect((self.host, self.port))
            
            cert = self.ssl_socket.getpeercert()
            print(f"Connected securely to {self.host}")
            print(f"Certificate: {cert.get('subject', 'Unknown')}")
            
            return True
        except Exception as e:
            print(f"Error connecting: {e}")
            return False
    
    def send_message(self, message: str) -> bool:
        """Отправка сообщения"""
        try:
            if self.ssl_socket:
                self.ssl_socket.send(message.encode())
                return True
            return False
        except Exception as e:
            print(f"Error sending: {e}")
            return False
    
    def close(self):
        """Закрытие соединения"""
        if self.ssl_socket:
            self.ssl_socket.close()
        if self.socket:
            self.socket.close()


print("Client created with SSL/TLS support")


# ==============================================================================
# УПРАЖНЕНИЕ 3: HMAC Message Authentication
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 3: HMAC Message Authentication")
print("=" * 60)


class HMACAuthenticator:
    """Аутентификация сообщений с использованием HMAC"""
    
    def __init__(self, secret_key: bytes):
        self.secret_key = secret_key
    
    def generate_hmac(self, message: str) -> str:
        """Генерация HMAC для сообщения"""
        h = hmac.new(
            self.secret_key,
            message.encode(),
            hashlib.sha256
        )
        return h.hexdigest()
    
    def verify_hmac(self, message: str, hmac_to_verify: str) -> bool:
        """Проверка HMAC"""
        expected_hmac = self.generate_hmac(message)
        return hmac.compare_digest(expected_hmac, hmac_to_verify)
    
    def create_signed_message(self, message: str) -> Tuple[str, str]:
        """Создание подписанного сообщения"""
        hmac_value = self.generate_hmac(message)
        return message, hmac_value
    
    def verify_signed_message(self, message: str, hmac_value: str) -> bool:
        """Проверка подписанного сообщения"""
        return self.verify_hmac(message, hmac_value)


key = b"super_secret_key_12345"
auth = HMACAuthenticator(key)

message = "Transfer $1000 to account 12345"
signed_message, hmac_value = auth.create_signed_message(message)

print(f"Original message: {signed_message}")
print(f"HMAC: {hmac_value}")

is_valid = auth.verify_signed_message(signed_message, hmac_value)
print(f"Signature valid: {is_valid}")

tampered_message = "Transfer $9999 to account 12345"
is_tampered = auth.verify_signed_message(tampered_message, hmac_value)
print(f"Tampered message detected: {not is_tampered}")


# ==============================================================================
# УПРАЖНЕНИЕ 4: Port Scanner with Service Detection
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 4: Port Scanner with Service Detection")
print("=" * 60)


class SecurePortScanner:
    """Сканер портов с определением сервисов"""
    
    COMMON_PORTS = {
        20: 'FTP-DATA',
        21: 'FTP',
        22: 'SSH',
        23: 'TELNET',
        25: 'SMTP',
        53: 'DNS',
        80: 'HTTP',
        110: 'POP3',
        143: 'IMAP',
        443: 'HTTPS',
        445: 'SMB',
        993: 'IMAPS',
        995: 'POP3S',
        3306: 'MySQL',
        3389: 'RDP',
        5432: 'PostgreSQL',
        5900: 'VNC',
        6379: 'Redis',
        8080: 'HTTP-ALT',
        8443: 'HTTPS-ALT',
        27017: 'MongoDB'
    }
    
    def __init__(self, timeout: float = 1.0):
        self.timeout = timeout
    
    def scan_port(self, host: str, port: int) -> Dict[str, Any]:
        """Сканирование одного порта"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            
            is_open = result == 0
            
            return {
                'port': port,
                'open': is_open,
                'service': self.COMMON_PORTS.get(port, 'UNKNOWN'),
                'secure': port in [443, 8443, 993, 995]
            }
        except Exception as e:
            return {'port': port, 'open': False, 'error': str(e)}
    
    def scan_host(self, host: str, ports: List[int] = None) -> List[Dict[str, Any]]:
        """Сканирование хоста"""
        if ports is None:
            ports = list(self.COMMON_PORTS.keys())
        
        results = []
        for port in ports:
            result = self.scan_port(host, port)
            if result['open']:
                results.append(result)
        
        return results
    
    def generate_report(self, scan_results: List[Dict[str, Any]]) -> str:
        """Генерация отчёта"""
        report = []
        report.append("=" * 50)
        report.append("Port Scan Report")
        report.append("=" * 50)
        
        open_ports = [r for r in scan_results if r['open']]
        report.append(f"\nOpen ports: {len(open_ports)}")
        
        insecure = [r for r in open_ports if not r['secure']]
        report.append(f"Insecure services: {len(insecure)}")
        
        for result in open_ports:
            status = "SECURE" if result['secure'] else "INSECURE"
            report.append(f"  Port {result['port']}: {result['service']} [{status}]")
        
        return "\n".join(report)


scanner = SecurePortScanner(timeout=0.5)
print("Scanning localhost (127.0.0.1):")

results = scanner.scan_host('127.0.0.1', [22, 80, 443, 8080])
for result in results:
    print(f"  Port {result['port']}: {result['service']} - Open")


print("\n" + "=" * 60)
print("Все упражнения выполнены!")
print("=" * 60)
