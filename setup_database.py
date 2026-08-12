from pathlib import Path
import sqlite3
ROOT=Path(__file__).resolve().parent
DB=ROOT/'database'/'ecsales.db'
print(f"Database is already included at: {DB}")
print("No Oracle, MySQL, PostgreSQL, Docker, or database server is required.")
print("To inspect it manually, install DB Browser for SQLite (optional), then open ecsales.db.")
