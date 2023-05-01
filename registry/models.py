from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from uuid import uuid4
# Create your models here.

   

class Subscriber(models.Model):
    
    class ONDCDomainType(models.TextChoices):
        MOBILITY = 'mobility'
        LOGISTICS = 'logistics'
        RETAIL = 'retail'
    
    class SubscriberType(models.TextChoices):
        BAP = "BAP"
        BPP = 'BPP'
        BG = 'BG'
    
    class SubscriptionStatus(models.TextChoices):
        INITIATED = 'INITIATED'
        UNDER_SUBSCRIPTION = 'UNDER_SUBSCRIPTION'
        SUBSCRIBED = 'SUBSCRIBED'
        INVALID_SSL = 'INVALID_SSL'
        UNSUBSCRIBED = 'UNSUBSCRIBED'
        


    subscriber_id = models.CharField(max_length=265, primary_key=True, editable=False)
    callback_url = models.FilePathField(unique=True, blank=False, null=False)
    subscriber_url = models.FilePathField(blank=False, null=False)
    country = models.CharField(max_length=3, blank=False, null=False)
    city = models.CharField(max_length=4,db_index=True, blank=False, null=False)
    domain = models.CharField(max_length=10, choices=ONDCDomainType.choices, 
                              db_index=True, blank=False, null=False)
    signing_public_key = models.CharField(
        max_length=64,
        unique=True, blank=False, null=False,
        editable=False
    )
    encryption_public_key = models.CharField(
        max_length=64,
        unique=True, blank=False, null=False,
        editable=False
    )
    valid_from = models.DateTimeField(blank=False, null=False)
    valid_until = models.DateTimeField(blank=False, null=False)
    legal_entity_name = models.TextField(blank=False, null=False)
    city_code = ArrayField(models.CharField(max_length=10), db_index=True, blank=False, null=False)
    gst = JSONField(default=dict, blank=False, null= False)
    pan = JSONField(default=dict, blank=False, null=False)
    owner_details = JSONField(default=dict, blank=False, null=False)
    name_of_authorised_signatory = models.CharField(max_length=80)
    address_of_authorised_signatory = models.TextField()
    email_id = models.EmailField()
    mobile_no = models.CharField(max_length=10)
    type = models.CharField(max_length=10, 
                            choices=SubscriberType.choices, db_index=True,
                            blank=True, null=True  
                        )
    unique_key_id = models.CharField(max_length=70, unique=True, blank=False, null=False)
    status = models.CharField(max_length=20, blank=False, null=False, 
                              choices=SubscriptionStatus.choices,
                              default=SubscriptionStatus.INITIATED
                            )
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)


class NetworkParticipant(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE, related_name='network_participant')
    subscriber_url = models.FilePathField(
        null=True,
        blank=True,
    )
    domain = models.CharField(max_length=10, choices=Subscriber.ONDCDomainType.choices, 
                              db_index=True, blank=False, null=False)
    type = models.CharField(max_length=10, 
                            choices=Subscriber.SubscriberType.choices, db_index=True,
                            blank=True, null=True  
                        )
    msn = models.BooleanField(default=False)
    city_code = ArrayField(models.CharField(max_length=10), db_index=True, blank=False, null=False)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)


class SellerOnRecord(models.Model):
    unique_key_id = models.CharField(max_length=100, primary_key=True)
    network_participant = models.ForeignKey(NetworkParticipant, on_delete=models.CASCADE, related_name='seller_on_record')
    signing_public_key = models.CharField(
        max_length=64,
        unique=True, blank=False, null=False
    )
    encryption_public_key = models.CharField(
        max_length=64,
        unique=True, blank=False, null=False
    )
    valid_from = models.DateTimeField(blank=False, null=False)
    valid_until = models.DateTimeField(blank=False, null=False)
    city_code = ArrayField(models.CharField(max_length=10), db_index=True, blank=False, null=False)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)
 



    
