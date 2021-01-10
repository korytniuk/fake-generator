from celery.utils.log import get_task_logger
from celery import shared_task

from .generator import generate_csvfile

logger = get_task_logger(__name__)


@shared_task
def generate_fake_file(dataset_id, rows):
    """generates a fake csv file with speicified number of rows"""
    return generate_csvfile(int(dataset_id), int(rows))
