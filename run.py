# run.py  (development only — has the debugger, auto-reload, verbose errors)
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5050)