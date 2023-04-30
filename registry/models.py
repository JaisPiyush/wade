from django.db import models

# Create your models here.

class Subscriber(models.Model):
    
    class ONDCDomainType(models.TextChoices):
        MOBILITY = 'mobility'
        LOGISTICS = 'logistics'
        RETAIL = 'retail'

    subscriber_id = models.CharField(max_length=75, primary_key=True)
    country = models.CharField(max_length=3)
    city = models.CharField(max_length=4,db_index=True)
    domain = models.CharField(max_length=10, choices=ONDCDomainType.choices, db_index=True)
    signing_public_key = models.CharField()


    
