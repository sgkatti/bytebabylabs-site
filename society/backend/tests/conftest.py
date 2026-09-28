import os

os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite:////tmp/society_task_platform_test.db")
os.environ.setdefault("SESSION_SECRET", "test-session-secret")
os.environ.setdefault("FRONTEND_ORIGIN", "http://testserver")
os.environ.setdefault("SECURE_COOKIES", "false")
