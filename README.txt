THREADFLOW - MULTI-THREADED JOB PROCESSING SYSTEM

1. Extract this folder.
2. Open the extracted MULTITHREADED_JOB_SYSTEM_FIXED folder in VS Code.
3. Open a terminal in this folder.
4. Activate your existing virtual environment if you have one:
   Windows CMD: venv\Scripts\activate
   PowerShell: .\venv\Scripts\Activate.ps1
5. If Flask is not installed: python -m pip install -r requirements.txt
6. Run: python app.py
7. Open: http://127.0.0.1:5000

This version fixes the shared layout for Dashboard, Submit Job and Job Queue.
Jobs are stored in database/jobs.db and persist after refresh.
At this stage jobs are saved with Pending status; worker execution is a later feature.
