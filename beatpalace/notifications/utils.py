from .models import Notification


def create_notification(
    *,
    recipient,
    sender=None,
    notification_type,
    title,
    message="",
    collaboration=None,
):

    return Notification.objects.create(
        recipient=recipient,
        sender=sender,
        notification_type=notification_type,
        title=title,
        message=message,
        collaboration=collaboration,
    )