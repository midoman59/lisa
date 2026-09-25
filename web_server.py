#!/usr/bin/env python3
"""Serveur web local de l'interface Lisa."""

import json
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WEB_DIR = ROOT / "web"
sys.path.insert(0, str(ROOT / "src"))

from agent.agent_data import DataAgent  # noqa: E402
from agent.data_loader import DataLoader  # noqa: E402

loader = DataLoader()
agent = None


def get_agent() -> DataAgent:
    global agent
    if agent is None:
        agent = DataAgent()
    return agent


class LisaHandler(BaseHTTPRequestHandler):
    def _send_json(self, payload: dict, status: int = 200) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, path: Path, content_type: str) -> None:
        if not path.is_file():
            self.send_error(404)
            return
        body = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if self.path == "/" or self.path == "/index.html":
            self._send_file(WEB_DIR / "index.html", "text/html; charset=utf-8")
        elif self.path == "/static/styles.css":
            self._send_file(WEB_DIR / "styles.css", "text/css; charset=utf-8")
        elif self.path == "/static/app.js":
            self._send_file(WEB_DIR / "app.js", "application/javascript; charset=utf-8")
        elif self.path == "/static/logo-societe-generale.png":
            self._send_file(WEB_DIR / "assets" / "logo-societe-generale.png", "image/png")
        elif self.path == "/api/dashboard":
            data_source = "Données mock locales (Azure AI Search RAG connecté pour le contexte documentaire)"
            if os.environ.get("DATA_SOURCE", "json").lower() == "postgres":
                data_source = "Données PostgreSQL Azure (RAG documentaire Azure AI Search séparé)"
            payload = {
                "stats": loader.get_statistics(),
                "total_evenements": len(loader.evenements),
                "dossiers": loader.get_dossiers(),
                "data_source_label": data_source,
            }
            self._send_json(payload)
        else:
            self.send_error(404)

    def do_POST(self) -> None:
        if self.path != "/api/chat":
            self.send_error(404)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length))
            user_question = str(payload.get("question", "")).strip()
            if not user_question:
                self._send_json({"error": "La question est vide."}, 400)
                return
            answer = get_agent().query(user_question)
            self._send_json({"answer": answer})
        except Exception as error:
            self._send_json({"error": str(error)}, 500)

    def log_message(self, format: str, *args: object) -> None:
        print(f"[WEB] {format % args}")


def main() -> None:
    server = ThreadingHTTPServer(("127.0.0.1", 8000), LisaHandler)
    print("Lisa IHM disponible sur http://127.0.0.1:8000")
    print("Appuyez sur Ctrl+C pour arrêter.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nArrêt du serveur.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
