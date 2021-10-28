from pyfcm import FCMNotification

from application.app import create_celery_app

celery = create_celery_app()


@celery.task()
def send_push_notification(registration_ids, data_to_send, ttl, fcm_api_key, fcm_proxy=None):
    push_service = FCMNotification(api_key=fcm_api_key, proxy_dict=fcm_proxy) if fcm_proxy else FCMNotification(
        api_key=fcm_api_key)

    push_result = push_service.multiple_devices_data_message(
        registration_ids=registration_ids,
        data_message=data_to_send,
        content_available=True,
        time_to_live=ttl
    ) if len(registration_ids) > 1 else push_service.single_device_data_message(
        registration_id=''.join(registration_ids),
        content_available=True,
        data_message=data_to_send,
        time_to_live=ttl
    )
