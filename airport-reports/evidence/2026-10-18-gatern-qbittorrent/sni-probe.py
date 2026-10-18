import concurrent.futures
import datetime
import json
import re
import socket
import ssl
import time

PROXY = ("172.25.64.1", 7890)
EDGE_IP = "172.67.160.99"
HOST = "qbittorrent.99010101.xyz"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"

def probe(sni, host=HOST, path="/"):
    start = time.monotonic()
    result = {"time": datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(), "proxy": PROXY[0], "connect": EDGE_IP, "sni": sni, "host": host, "path": path}
    sock = None
    try:
        sock = socket.create_connection(PROXY, timeout=12)
        sock.sendall(f"CONNECT {EDGE_IP}:443 HTTP/1.1\r\nHost: {EDGE_IP}:443\r\n\r\n".encode())
        response = b""
        while b"\r\n\r\n" not in response:
            chunk = sock.recv(1)
            if not chunk:
                raise EOFError("proxy closed before CONNECT response")
            response += chunk
        result["connect_status"] = response.split(b"\r\n")[0].decode()
        if b" 200 " not in response.split(b"\r\n")[0]:
            return result
        ctx = ssl.create_default_context()
        ctx.set_alpn_protocols(["http/1.1"])
        sock = ctx.wrap_socket(sock, server_hostname=sni)
        result["tls"] = sock.version()
        result["cipher"] = sock.cipher()[0]
        result["certificate_issuer"] = sock.getpeercert().get("issuer")
        sock.sendall(f"GET {path} HTTP/1.1\r\nHost: {host}\r\nUser-Agent: {UA}\r\nConnection: close\r\n\r\n".encode())
        data = b""
        while len(data) < 32768:
            chunk = sock.recv(4096)
            if not chunk:
                break
            data += chunk
        text = data.decode(errors="replace")
        result["http"] = text.split("\r\n")[0]
        result["title"] = re.findall(r"<title>(.*?)</title>", text)
        result["cf_ray"] = re.findall(r"(?im)^cf-ray:\s*([^\r\n]+)", text)
        if path == "/cdn-cgi/trace":
            result["trace"] = dict(re.findall(r"(?m)^(ip|colo|tls|sni)=([^\r\n]+)", text))
    except Exception as e:
        result["error"] = type(e).__name__ + ": " + str(e)
    finally:
        if sock:
            sock.close()
        result["elapsed_s"] = round(time.monotonic() - start, 3)
    return result

if __name__ == "__main__":
    names = ["grafana", "qbittorrent", "qbit", "torrent", "bittorrent", "bt"]
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        for result in executor.map(probe, [name + ".99010101.xyz" for name in names]):
            print(json.dumps(result, ensure_ascii=False), flush=True)
