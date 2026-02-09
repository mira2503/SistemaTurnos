from celery import shared_task
from .services import NotificationService
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def send_notifications_task(self, notification_ids=None):
    """
    Celery task to send notifications in the background.
    """
    try:
        logger.info(f"Starting background notification task for IDs: {notification_ids}")
        enviados, errores = NotificationService.ejecutar_vigilancia(specific_ids=notification_ids)
        logger.info(f"Background notification task finished. Sent: {enviados}, Errors: {errores}")
        return {'sent': enviados, 'errors': errores}
    except Exception as exc:
        logger.error(f"Error in background notification task: {exc}")
        raise self.retry(exc=exc, countdown=60)

@shared_task
def sync_notification_queue_task():
    """
    Periodic task to sync the notification queue with upcoming turns.
    """
    try:
        creadas = NotificationService.sincronizar_cola()
        synced, stuck = NotificationService.fix_turno_sync()
        logger.info(f"Sync task finished: Created {creadas}, Synced {synced}, Fixed {stuck}")
        return {'created': creadas, 'synced': synced, 'fixed': stuck}
    except Exception as e:
        logger.error(f"Error in sync notification queue task: {e}")
        return {'error': str(e)}
