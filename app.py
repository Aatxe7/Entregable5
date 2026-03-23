import os
from datetime import datetime
from flask import Flask, jsonify, request
from sqlalchemy import create_engine, text

def create_app():
    app = Flask(__name__)

    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        user = os.environ.get("DB_USER", "appuser")
        pwd = os.environ.get("DB_PASSWORD", "apppass")
        host = os.environ.get("DB_HOST", "db")
        port = os.environ.get("DB_PORT", "5432")
        name = os.environ.get("DB_NAME", "appdb")
        database_url = f"postgresql+psycopg://{user}:{pwd}@{host}:{port}/{name}"

    engine = create_engine(database_url, pool_pre_ping=True)

    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS notes (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL
            );
        """))

    @app.get("/")
    def root():
        return "Entregable 5 OK — Flask + PostgreSQL + Docker Compose + Azure CI/CD", 200

    @app.get("/health")
    def health():
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return jsonify(status="ok", db="ok", ts=datetime.utcnow().isoformat()), 200
        except Exception as e:
            return jsonify(status="error", db="error", error=str(e)), 500

    @app.post("/notes")
    def create_note():
        payload = request.get_json(silent=True) or {}
        title = (payload.get("title") or "").strip()
        if not title:
            return jsonify(error="title is required"), 400
        with engine.begin() as conn:
            row = conn.execute(
                text("INSERT INTO notes (title, created_at) VALUES (:t, :c) RETURNING id"),
                {"t": title, "c": datetime.utcnow()},
            ).fetchone()
        return jsonify(id=row[0], title=title), 201

    @app.get("/notes")
    def list_notes():
        with engine.connect() as conn:
            rows = conn.execute(text("SELECT id, title, created_at FROM notes ORDER BY id DESC LIMIT 50")).fetchall()
        return jsonify([{"id": r[0], "title": r[1], "created_at": r[2].isoformat()} for r in rows]), 200

    return app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("APP_PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=False)
