# wsgi.py  (production — this is what you'll actually deploy)
from waitress import serve
from app import create_app
import os

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"Starting production server with Waitress on port {port}...")
    serve(app, host="0.0.0.0", port=port, threads=4)