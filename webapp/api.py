from fastapi import FastAPI
from prometheus_client import make_asgi_app, Gauge
import httpx

app = FastAPI()
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

node_up = Gauge("proxmox_node_up", "Node reachable", ["node"])

NODES = {"webserver": "http://webserver:80", "grafana": "http://grafana:3000"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/nodes")
async def check_nodes():
    results = {}
    for node, url in NODES.items():
        try:
            async with httpx.AsyncClient(timeout=3) as c:
                await c.get(url)
                node_up.labels(node=node).set(1)
                results[node] = "up"
        except Exception:
            node_up.labels(node=node).set(0)
            results[node] = "down"
    return results