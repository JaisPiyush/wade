from typing import Any
from .models import * 
from rest_framework import serializers
from rest_framework import validators
from monitor.models import ContractRequestLogger
from django.conf import settings
from datetime import datetime, timedelta

# TODO: Validate city code

class KeyPairDetailSerializer(serializers.Serializer):
    signing_public_key = serializers.CharField(required=True)
    encryption_public_key = serializers.CharField(required=True)
    valid_from = serializers.DateTimeField(required=True)
    valid_until = serializers.DateTimeField(required=True)

class SellerOnRecordSerializer(serializers.ModelSerializer):

    key_pair = KeyPairDetailSerializer()

    class Meta:
        model = SellerOnRecord
        fields = '__all__'
        write_only_fields = ('network_participant',)
        read_only_fields = ('created', 'updated')
    

class NetworkParticipantSerializer(serializers.ModelSerializer):
    seller_on_record = SellerOnRecordSerializer(many=True,allow_empty=True, required=False,
                        allow_null=False)
    class Meta:
        model = NetworkParticipant
        exclude = ('subscriber',)
        read_only_fields = ('created', 'updated')
    
    def validate_msn(self, value):
        if value and self.fields['type'] != Subscriber.SubscriberType.BPP:
            raise serializers.ValidationError('Invalid field value, only BPP can have msn=true')
        return value
    
    def validate_seller_on_record(self, value):
        if len(value) > 0 and (self.fields['type'] != Subscriber.SubscriberType.BPP \
            or not self.fields['msn']):
            raise serializers.ValidationError('This field is unacceptable, only BPP-MSN can create this.')
        return value
    
    def create(self, subscriber: Subscriber, validated_data: Any) -> Any:
        return NetworkParticipant.objects.create(subscriber=subscriber, **validated_data)


class GSTDetailSerializer(serializers.Serializer):
    legal_entity_name = serializers.CharField(required=True)
    business_address = serializers.CharField(required=True)
    city_code = serializers.ListField(child=serializers.CharField(), required=True)
    gst_no = serializers.CharField(required=True)

class PanDetailSerializer(serializers.Serializer):
    name_as_per_pan = serializers.CharField(required=True)
    pan_no = serializers.CharField(required=True)
    date_of_incorporation = serializers.CharField(required=True)


class SubscriberSerializer(serializers.ModelSerializer):
    gst = GSTDetailSerializer(required=True)
    pan = PanDetailSerializer(required=True)
    key_pair = KeyPairDetailSerializer()

    class Meta:
        model = Subscriber
        fields = '__all__'
        read_only_fields = ('status', 'created', 'updated')


class WriteSubscriberOperationNumberSerializer(serializers.Serializer):
    ops_no = serializers.IntegerField(
        required=True,
        min_value=1,
        max_value=10
    )

class WriteSubscriberContextSerializer(serializers.Serializer):
    operation = WriteSubscriberOperationNumberSerializer(required=True)

class WriteSubscriberMessageSerializer(serializers.Serializer):
    request_id = serializers.CharField(required=True, validators=[
        validators.UniqueValidator(ContractRequestLogger.objects.filter(target=settings.HOSTNAME))
    ])
    timestamp = serializers.DateTimeField(required=True)
    entity = SubscriberSerializer(required=True)
    network_participant = serializers.ListField(child=NetworkParticipantSerializer(), required=True)

    def validate_timestamp(self, value: datetime):
        if datetime.now(value.tzinfo) > value + timedelta(seconds=30):
            raise serializers.ValidationError(f'The request has expired. Max validity of any request is 30s')

 
class WriteSubscriberSerializer(serializers.Serializer):
    context = WriteSubscriberContextSerializer(required=True)
    message = WriteSubscriberMessageSerializer(required=True)


    #TODO: Add update function (subscriber details, network participant, seller_on_record)
    def create(self, validated_data):
        subscriber = self.message.entity.create(validated_data['message']['entity'])
        NetworkParticipant.objects.bulk_create(
            [NetworkParticipant(subscriber=subscriber, **participant.validated_data
                                ) for participant in self.message.network_participant]
        )
        return subscriber
        # TODO: Queue post processing
    # Only updates the Subscriber model
    def update(self, instance: Any, validated_data: Any) -> Subscriber:
        return self.message.entity.update(instance, validated_data['message']['entity'])

# TODO: API to PUT, PATCH seller_on_record in subscriber
# TODO: API to PUT, PATCH network participant
# TODO: Authentication to perform updates 
#TODO: Add queue process to validate subscriber whitelisting on ONDC site


