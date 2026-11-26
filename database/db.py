import os
import sqlite3

DATABASE_PATH = os.path.join(os.path.dirname(__file__), "jobs.db")

def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection

def initialize_database():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                priority TEXT NOT NULL,
                status TEXT DEFAULT 'Pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                started_at TIMESTAMP,
                completed_at TIMESTAMP,
                worker_id TEXT,
                execution_time REAL,
                error_message TEXT
            )
        """)

def create_job(name, description, priority):
    with get_connection() as connection:
        cursor = connection.execute(
            "INSERT INTO jobs (name, description, priority) VALUES (?, ?, ?)",
            (name, description, priority)
        )
        return cursor.lastrowid

def get_all_jobs():
    with get_connection() as connection:
        rows = connection.execute("SELECT * FROM jobs ORDER BY id DESC").fetchall()
        return [dict(row) for row in rows]

def get_job_counts():
    with get_connection() as connection:
        total, pending, running, completed, failed = connection.execute("""
            SELECT COUNT(*),
                   SUM(CASE WHEN status='Pending' THEN 1 ELSE 0 END),
                   SUM(CASE WHEN status='Running' THEN 1 ELSE 0 END),
                   SUM(CASE WHEN status='Completed' THEN 1 ELSE 0 END),
                   SUM(CASE WHEN status='Failed' THEN 1 ELSE 0 END)
            FROM jobs
        """).fetchone()
    return {
        "total": total or 0,
        "pending": pending or 0,
        "running": running or 0,
        "completed": completed or 0,
        "failed": failed or 0
    }


def get_worker_performance():

    connection = get_connection()

    try:
        rows = connection.execute("""
            SELECT
                worker_id,
                COUNT(*) AS completed_jobs,
                ROUND(AVG(execution_time), 2) AS avg_execution_time,
                ROUND(SUM(execution_time), 2) AS total_execution_time
            FROM jobs
            WHERE status = 'Completed'
            AND worker_id IS NOT NULL
            GROUP BY worker_id
            ORDER BY worker_id
        """).fetchall()

        return [dict(row) for row in rows]

    finally:
        connection.close()


def get_job_by_id(job_id):
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM jobs WHERE id = ?",
            (job_id,)
        ).fetchone()

        return dict(row) if row else None


def cancel_job(job_id):
    with get_connection() as connection:
        cursor = connection.execute(
            """
            UPDATE jobs
            SET status = 'Cancelled'
            WHERE id = ? AND status = 'Pending'
            """,
            (job_id,)
        )

        return cursor.rowcount > 0


def retry_job(job_id):
    with get_connection() as connection:
        cursor = connection.execute(
            """
            UPDATE jobs
            SET status = 'Pending',
                worker_id = NULL,
                started_at = NULL,
                completed_at = NULL,
                execution_time = NULL,
                error_message = NULL
            WHERE id = ? AND status = 'Failed'
            """,
            (job_id,)
        )

        return cursor.rowcount > 0




