from celery import shared_task, current_task
from celery_progress.backend import ProgressRecorder, Progress
import time


@shared_task(bind=True)
def my_task(self, row, total):
    progress_recorder = ProgressRecorder(self)
    progress_recorder.set_progress(row, total)
    return row



