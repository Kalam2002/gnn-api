import requests
import random

url = "http://127.0.0.1:8000/predict"

def generate_flow():
    return {
        "src_ip": f"192.168.1.{random.randint(1,255)}",
        "src_port": random.randint(1000,9999),
        "dst_ip": "192.168.1.1",
        "dst_port": random.choice([80, 22, 443, 53]),
        "proto": random.choice(["tcp", "udp"]),
        "service": random.choice(["http", "ssh", "dns"]),
        "duration": random.random()*5,
        "src_bytes": random.randint(100,10000),
        "dst_bytes": random.randint(50,5000),
        "conn_state": random.choice(["SF","S0","REJ"]),
        "src_pkts": random.randint(1,100),
        "dst_pkts": random.randint(1,100)
    }

for _ in range(10):
    data = {"flows": [generate_flow() for _ in range(5)]}
    res = requests.post(url, json=data)
    print(res.json())