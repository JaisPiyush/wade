from django.db import models

# Create your models here.

class ContractRequestLogger(models.Model):
    target = models.CharField(max_length=265, editable=False)
    origin = models.CharField(max_length=265, editable=False)
    request_id = models.CharField(max_length=80, primary_key=True)
    created = models.DateTimeField(auto_created=True, editable=False)

    class Meta:
        indexes = [
            models.Index(fields=['target', 'origin'])
        ]
