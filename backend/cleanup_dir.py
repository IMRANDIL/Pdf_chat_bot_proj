import os
import schedule
import time

UPLOAD_FOLDER = './source'  # The folder where the PDFs are stored

def clean_upload_folder():
    try:
        # Check if the folder exists
        if os.path.exists(UPLOAD_FOLDER):
            # List all files in the folder
            for filename in os.listdir(UPLOAD_FOLDER):
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                try:
                    # Remove only files (not directories)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        print(f"Removed file: {file_path}")
                except Exception as e:
                    print(f"Failed to remove {file_path}. Reason: {e}")
    except Exception as e:
        print(f"Error cleaning upload folder: {e}")

# Scheduler function to run every 2 hours
def schedule_cleanup():
    schedule.every(15).minutes.do(clean_upload_folder)

    while True:
        schedule.run_pending()
        time.sleep(1)
