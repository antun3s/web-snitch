# Web Snitch

A minimal Docker container that displays server and client connection information.

## What it does

When accessed, it returns plain text with Server info(IP, hostname and uptime) and Client(IP and header).

## How to use

   ```bash
    docker run -d -p 8080:8080 --name snitch web-snitch
   ```

Access it:

- Browser: http://localhost:8080

- cli 
   ```bash
   curl http://localhost:8080
   ```

Example output
   ```text
Server:
- IP: 172.17.0.2
- Hostname: b8373070028e
- Uptime: 2 days, 19:34:51
Client:
- IP: 172.17.0.1
- Header: 127.0.0.1:8082
   ```

Technical details
- Image size: ~61MB
- Based on Python 3.12 Alpine
- Uses Flask for web server
- No styling, just plain text
