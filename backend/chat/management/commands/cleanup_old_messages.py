from django.core.management.base import BaseCommand
from chat.models import Message
from django.utils import timezone
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Cleanup messages older than 3 days and delete associated files'

    def handle(self, *args, **options):
        cutoff = timezone.now() - timezone.timedelta(days=3)
        old = Message.objects.filter(created_at__lt=cutoff)
        count = old.count()
        for m in old:
            if m.image and m.image.path and os.path.exists(m.image.path):
                try:
                    os.remove(m.image.path)
                except Exception:
                    pass
            m.delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted {count} messages and files'))
