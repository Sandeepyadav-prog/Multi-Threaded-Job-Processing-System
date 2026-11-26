# ⚙️ ThreadFlow – Multi-Threaded Job Processing System

A Python Flask-based web application that demonstrates the practical implementation of Operating System concepts through multithreaded job processing, concurrency, synchronization, and priority-based job management.

## 📌 Project Overview

ThreadFlow is a web-based job processing system designed to manage and execute multiple jobs using background worker threads.

The application allows users to submit jobs, monitor their execution, manage job priorities, view execution history, and analyze worker performance through an interactive dashboard.

It demonstrates how multiple threads can process jobs concurrently while maintaining synchronization and managing shared resources.

## ✨ Features

- **Interactive Dashboard:** Displays total jobs, completed jobs, pending jobs, and running jobs.
- **Job Submission:** Submit new jobs with a name, description, and priority.
- **Job Queue Management:** View and manage submitted jobs.
- **Search and Filtering:** Search jobs and filter them according to status and priority.
- **Multithreaded Processing:** Uses three background worker threads to process jobs.
- **Priority-Based Processing:** Supports High, Medium, and Low priority jobs.
- **Worker Monitoring:** Monitor worker status and assigned jobs.
- **Job Details:** View detailed information about individual jobs.
- **Job Cancellation:** Cancel pending jobs.
- **Job Retry:** Provides functionality to retry failed jobs.
- **Execution History:** View previously processed jobs.
- **Worker Analytics:** Analyze worker performance and execution statistics.
- **Database Integration:** Stores job information using SQLite.

## 🧠 Operating System Concepts Implemented

| OS Concept | Implementation |
|---|---|
| Multithreading | Multiple worker threads execute jobs |
| Concurrency | Multiple workers process jobs independently |
| Synchronization | Threading Lock protects shared data |
| Producer-Consumer Problem | Queue manages communication between job submission and workers |
| Thread Management | Python threading module |
| Priority-Based Processing | Jobs are selected according to priority |
| Shared Resources | Workers access common job-management data |

## 🛠️ Technologies Used

**Frontend**
- HTML5
- CSS3
- JavaScript
- Chart.js

**Backend**
- Python 3.12
- Flask
- Python Threading
- Queue Module

**Database**
- SQLite

**Development Tools**
- Visual Studio Code
- Git
- GitHub

## 📂 Project Structure

```text
MULTITHREADED_JOB_SYSTEM/
│
├── app.py
├── worker_manager.py
├── requirements.txt
│
├── database/
│   └── db.py
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── submit_job.html
│   ├── job_queue.html
│   ├── job_details.html
│   ├── worker_monitor.html
│   ├── execution_history.html
│   └── worker_analytics.html
│
├── static/
│   └── css/
│       └── style.css
│
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Sandeepyadav-prog/Multi-Threaded-Job-Processing-System.git
```

### 2. Navigate to the Project Directory

```bash
cd Multi-Threaded-Job-Processing-System
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

For Windows:

```bash
venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Application

```bash
python app.py
```

### 7. Open in Browser

Visit:

```text
http://127.0.0.1:5000
```

## 🔄 How the System Works

1. The user submits a job through the web interface.
2. The application stores job information in the SQLite database.
3. Jobs are selected according to their priority.
4. The job IDs are placed into a thread-safe queue.
5. Three background worker threads retrieve jobs from the queue.
6. A worker marks its assigned job as Running.
7. After the simulated processing period, the job status is updated to Completed.
8. The dashboard and analytics pages display updated information.

## 📊 Main Modules

| Module | Description |
|---|---|
| Dashboard | Displays overall job statistics |
| Submit Job | Allows users to submit new jobs |
| Job Queue | Displays jobs and provides search and filtering |
| Worker Monitor | Displays worker status |
| Job Details | Shows individual job information |
| Execution History | Displays completed and other recorded jobs |
| Worker Analytics | Shows worker performance statistics |

## ⚠️ Project Limitations

- Job execution is currently simulated using a five-second delay.
- Worker threads and the processing queue operate within the running application.
- Worker statistics are maintained in memory and reset when the application restarts.
- This project demonstrates application-level multithreading rather than a complete operating-system CPU scheduler.

## 🚀 Future Enhancements

- Implement real-world job execution tasks.
- Add user authentication and role-based access.
- Introduce advanced scheduling algorithms such as FCFS and Round Robin.
- Implement graceful worker shutdown and recovery.
- Add real-time monitoring and notifications.
- Improve database and queue persistence.
- Deploy the application on a cloud platform.

## 🎯 Project Objective

The main objective of ThreadFlow is to provide a practical understanding of Operating System concepts by developing a multithreaded job processing application with a user-friendly web interface.

## 👩‍💻 Developer

**Ayesha Rohilla**

B.Tech – Computer Science and Engineering (AI & ML)

K.R. Mangalam University

## 📜 License

This project is developed for academic and educational purposes.