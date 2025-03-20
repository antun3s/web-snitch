from flask import Flask, request
import socket
import os
from datetime import timedelta

app = Flask(__name__)

def get_server_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        return s.getsockname()[0]
    except:
        return '127.0.0.1'
    finally:
        s.close()

def get_process_uptime():
    try:
        # Ler o uptime do sistema
        with open('/proc/uptime', 'r') as f:
            system_uptime = float(f.readline().split()[0])
        
        # Ler informações do processo PID 1
        with open('/proc/1/stat', 'r') as f:
            data = f.read()
            # Extrair o tempo de início do processo (campo 22 após o nome)
            end_name = data.rfind(')')
            parts = data[end_name+1:].split()
            if len(parts) < 21:
                return timedelta(seconds=system_uptime)
            
            start_time_ticks = int(parts[19])
            clock_ticks = os.sysconf(os.sysconf_names['SC_CLK_TCK'])
            start_time_sec = start_time_ticks / clock_ticks
            process_uptime_sec = system_uptime - start_time_sec
            
            return timedelta(seconds=process_uptime_sec)
    
    except Exception as e:
        # Fallback para o uptime do sistema em caso de erro
        return timedelta(seconds=system_uptime)

@app.route('/')
def show_info():
    server_ip = get_server_ip()
    hostname = socket.gethostname()
    
    # Obter e formatar o uptime do processo
    uptime = get_process_uptime()
    uptime_str = str(uptime).split('.')[0]  # Remover frações de segundo
    
    client_ip = request.remote_addr
    host_header = request.headers.get('Host', '')
    
    return f"""
Server:
- IP: {server_ip}
- Hostname: {hostname}
- Uptime: {uptime_str}
Client:
- IP: {client_ip}
- Header: {host_header}
""", 200, {'Content-Type': 'text/plain; charset=utf-8'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
