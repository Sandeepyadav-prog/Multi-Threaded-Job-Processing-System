
from flask import Flask, render_template, request, redirect, flash, url_for

from database.db import (
    initialize_database,
    create_job,
    get_all_jobs,
    get_job_counts,
    get_worker_performance,
    get_job_by_id,
    cancel_job,
    retry_job
)

from worker_manager import worker_manager

app = Flask(__name__)
app.secret_key = "multithread_job_system_secret"

# Initialize SQLite database
initialize_database()


@app.route("/")
def home():

    jobs = get_all_jobs()
    counts = get_job_counts()

    return render_template(
        "index.html",
        jobs=jobs,
        counts=counts
    )


@app.route("/submit-job", methods=["GET", "POST"])
def submit_job():

    if request.method == "POST":

        job_name = request.form.get("job_name", "").strip()
        description = request.form.get("description", "").strip()
        priority = request.form.get("priority", "Medium")

        if not job_name or not description:

            flash("Please fill in all required fields.", "error")
            return redirect(url_for("submit_job"))

        if priority not in ["Low", "Medium", "High"]:

            flash("Invalid priority selected.", "error")
            return redirect(url_for("submit_job"))

        job_id = create_job(
            job_name,
            description,
            priority
        )

        flash(
            f"Job #{job_id} submitted successfully!",
            "success"
        )

        return redirect(url_for("submit_job"))

    return render_template("submit_job.html")



@app.route("/job-queue")
def job_queue():
    jobs = get_all_jobs()

    search_query = request.args.get("search", "").strip().lower()
    status_filter = request.args.get("status", "").strip()
    priority_filter = request.args.get("priority", "").strip()

    filtered_jobs = []

    for job in jobs:
        job_id = str(job["id"] or "").lower()
        job_name = str(job["name"] or "").lower()
        job_description = str(job["description"] or "").lower()

        # Search by Job ID, Job Name, or Description
        if search_query:
            if (search_query not in job_id
                    and search_query not in job_name
                    and search_query not in job_description):
                continue

        # Filter by Status
        if status_filter and str(job["status"]) != status_filter:
            continue

        # Filter by Priority
        if priority_filter and str(job["priority"]) != priority_filter:
            continue

        filtered_jobs.append(job)

    return render_template(
        "job_queue.html",
        jobs=filtered_jobs,
        search_query=request.args.get("search", "").strip(),
        status_filter=status_filter,
        priority_filter=priority_filter
    )


@app.route("/job-details/<int:job_id>")
def job_details(job_id):
    job = get_job_by_id(job_id)

    if job is None:
        flash("Job not found.", "error")
        return redirect(url_for("job_queue"))

    return render_template("job_details.html", job=job)


@app.route("/cancel-job/<int:job_id>", methods=["POST"])
def cancel_job_route(job_id):
    success = cancel_job(job_id)

    if success:
        flash("Job cancelled successfully.", "success")
    else:
        flash(
            "This job cannot be cancelled. Only Pending jobs can be cancelled.",
            "error"
        )

    return redirect(url_for("job_queue"))


@app.route("/retry-job/<int:job_id>", methods=["POST"])
def retry_job_route(job_id):
    success = retry_job(job_id)

    if success:
        flash("Job added back to the queue successfully.", "success")
    else:
        flash("Only Failed jobs can be retried.", "error")

    return redirect(url_for("job_queue"))




@app.route("/worker-monitor")
def worker_monitor():
    workers = worker_manager.get_worker_status()
    return render_template("worker_monitor.html", workers=workers)

@app.route("/execution-history")
def execution_history():
    jobs = get_all_jobs()
    return render_template("execution_history.html", jobs=jobs)

@app.route("/worker-analytics")
def worker_analytics():
    performance = get_worker_performance()

    return render_template(
        "worker_analytics.html",
        performance=performance
    )
@app.route("/start-workers", methods=["POST"])
def start_workers():

    added_jobs = worker_manager.start()

    if added_jobs > 0:

        flash(
            f"Workers started! {added_jobs} pending jobs added to processing.",
            "success"
        )

    else:

        flash(
            "Workers are ready, but there are no new pending jobs to process.",
            "error"
        )

    return redirect(url_for("job_queue"))


if __name__ == "__main__":

    app.run(
        debug=True,
        use_reloader=False
    )
