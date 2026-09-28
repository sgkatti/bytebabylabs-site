import os

os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite:///:memory:")
os.environ.setdefault("SESSION_SECRET", "test-session-secret")
os.environ.setdefault("FRONTEND_ORIGIN", "http://testserver")
os.environ.setdefault("SECURE_COOKIES", "false")
