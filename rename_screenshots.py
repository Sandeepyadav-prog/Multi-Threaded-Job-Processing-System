
import os

folder = "screenshots"

new_names = [
    "dashboard.png",
    "submit-job.png",
    "job-queue-filters.png",
    "job-queue-records.png",
    "job-details.png",
    "worker-monitor.png",
    "execution-history.png",
    "worker-analytics-overview.png",
    "worker-analytics-details.png"
]

files = sorted(
    f for f in os.listdir(folder)
    if f.lower().endswith((".png", ".jpg", ".jpeg"))
)

if len(files) != 9:
    print(f"Expected 9 screenshots, but found {len(files)}.")
    print("No files were renamed.")
    raise SystemExit

if any(os.path.exists(os.path.join(folder, name)) for name in new_names):
    print("A destination filename already exists.")
    print("No files were renamed. Please check the folder.")
    raise SystemExit

# Rename to temporary filenames first
temp_files = []

for i, filename in enumerate(files):
    old_path = os.path.join(folder, filename)
    temp_path = os.path.join(folder, f"temp_image_{i}.tmp")
    os.rename(old_path, temp_path)
    temp_files.append(temp_path)

# Assign final names
for temp_path, new_name in zip(temp_files, new_names):
    new_path = os.path.join(folder, new_name)
    os.rename(temp_path, new_path)
    print("Renamed:", new_name)

print("\nAll 9 screenshots renamed successfully!")
