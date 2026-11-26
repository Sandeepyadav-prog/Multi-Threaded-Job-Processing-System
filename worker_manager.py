import queue
import threading
import time

from database.db import get_connection


class WorkerManager:

    def __init__(self, worker_count=3):
        self.worker_count = worker_count
        self.job_queue = queue.Queue()
        self.lock = threading.Lock()
        self.threads = []
        self.started = False
        self.enqueued_ids = set()

        # Live worker information
        self.worker_status = {
            f"Worker-{number}": {
                "status": "Idle",
                "current_job": None,
                "completed_jobs": 0
            }
            for number in range(1, worker_count + 1)
        }

    def start(self):

        with self.lock:

            if not self.started:
                self.started = True

                for number in range(1, self.worker_count + 1):
                    worker_name = f"Worker-{number}"

                    worker = threading.Thread(
                        target=self.process_jobs,
                        args=(worker_name,),
                        daemon=True,
                        name=worker_name
                    )

                    worker.start()
                    self.threads.append(worker)

            connection = get_connection()

            try:
                pending_jobs = connection.execute("""
                    SELECT id FROM jobs
                    WHERE status = 'Pending'
                    ORDER BY
                    CASE priority
                        WHEN 'High' THEN 1
                        WHEN 'Medium' THEN 2
                        ELSE 3
                    END,
                    id ASC
                """).fetchall()

            finally:
                connection.close()

            added_jobs = 0

            for job in pending_jobs:
                job_id = job["id"]

                if job_id not in self.enqueued_ids:
                    self.enqueued_ids.add(job_id)
                    self.job_queue.put(job_id)
                    added_jobs += 1

            return added_jobs

    def process_jobs(self, worker_name):

        while True:

            job_id = self.job_queue.get()
            start_time = time.time()
            job_started = False

            try:
                connection = get_connection()

                try:
                    cursor = connection.execute("""
                        UPDATE jobs
                        SET status = 'Running',
                            started_at = CURRENT_TIMESTAMP,
                            worker_id = ?
                        WHERE id = ?
                        AND status = 'Pending'
                    """, (worker_name, job_id))

                    connection.commit()
                    job_started = cursor.rowcount > 0

                finally:
                    connection.close()

                if not job_started:
                    continue

                # Update live worker status
                with self.lock:
                    self.worker_status[worker_name]["status"] = "Working"
                    self.worker_status[worker_name]["current_job"] = job_id

                # Simulate job execution
                time.sleep(5)

                execution_time = round(time.time() - start_time, 2)

                connection = get_connection()

                try:
                    connection.execute("""
                        UPDATE jobs
                        SET status = 'Completed',
                            completed_at = CURRENT_TIMESTAMP,
                            execution_time = ?
                        WHERE id = ?
                    """, (execution_time, job_id))

                    connection.commit()

                finally:
                    connection.close()

                with self.lock:
                    self.worker_status[worker_name]["completed_jobs"] += 1

                print(
                    f"{worker_name} completed Job #{job_id} "
                    f"in {execution_time} seconds"
                )

            except Exception as error:

                connection = get_connection()

                try:
                    connection.execute("""
                        UPDATE jobs
                        SET status = 'Failed',
                            error_message = ?
                        WHERE id = ?
                    """, (str(error), job_id))

                    connection.commit()

                finally:
                    connection.close()

                print(f"{worker_name} failed Job #{job_id}: {error}")

            finally:

                with self.lock:
                    self.worker_status[worker_name]["status"] = "Idle"
                    self.worker_status[worker_name]["current_job"] = None
                    self.enqueued_ids.discard(job_id)

                self.job_queue.task_done()

    def get_worker_status(self):

        with self.lock:
            return {
                worker: details.copy()
                for worker, details in self.worker_status.items()
            }


worker_manager = WorkerManager(worker_count=3)