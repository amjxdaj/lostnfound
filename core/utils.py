from .models import LostItem
from difflib import SequenceMatcher
from django.core.mail import send_mail
from django.conf import settings

def find_matches(found_item):
    matches = []
    lost_items = LostItem.objects.all()

    for lost in lost_items:
        # Date check: skip if found date is earlier than lost date
        if found_item.date_found < lost.date_lost:
            continue

        # Combine title + description for better matching
        lost_text = (lost.title + " " + lost.description).lower()
        found_text = (found_item.title + " " + found_item.description).lower()

        # Text similarity
        text_ratio = SequenceMatcher(None, lost_text, found_text).ratio()

        # Location similarity
        loc_ratio = SequenceMatcher(None, lost.location.lower(), found_item.location.lower()).ratio()

        # Match if both text and location similarity are above threshold
        if text_ratio > 0.6 and loc_ratio > 0.6:
            matches.append(lost)

    return matches

from .models import Notification

def create_notification(user, message, link=None):
    Notification.objects.create(user=user, message=message, link=link)


def send_notification_email(to_email, subject, message):
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [to_email],
        fail_silently=False,
    )
