from buyboxpredictor.extensions import celery


@celery.task
def dummy_task():
    return "OK"
