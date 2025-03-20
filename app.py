from flask import Flask, request
import socket
from datetime import datetime, timedelta

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

@app.route('/')
def show_info():
    # Server info
    server_ip = get_server_ip()
    hostname = socket.gethostname()
    
    # Uptime calculation
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
    uptime = str(timedelta(seconds=uptime_seconds)).split('.')[0]
    
    # Client info
    client_ip = request.remote_addr
    host_header = request.headers.get('Host', '')
    
    return f"""
Server:
- IP: {server_ip}
- Hostname: {hostname}
- Uptime: {uptime}
Client:
- IP: {client_ip}
- Header: {host_header}
""", 200, {'Content-Type': 'text/plain; charset=utf-8'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
