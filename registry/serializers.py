from typing import Any
from .models import * 
from rest_framework import serializers
from rest_framework import validators
from monitor.models import ContractRequestLogger
from django.conf import settings
from datetime import datetime, timedelta


class SellerOnRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = SellerOnRecord
        write_only_fields = ('network_participant',)
    

class NetworkParticipantSerializer(serializers.ModelSerializer):
    seller_on_record = serializers.RelatedField(many=True)
    class Meta:
        model = NetworkParticipant
        write_only_fields = ('subscriber',)
    
    def validate_seller_on_record(self, value):
        if len(value) > 0 and (self.fields['type'] != Subscriber.SubscriberType.BPP \
            or not self.fields['msn']):
            raise serializers.ValidationError('This field is unacceptable, only BPP-MSN can create this.')
        return value     

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
    gst = GSTDetailSerializer(source='gst', required=True)
    pan = PanDetailSerializer(source='pan', required=True)

    class Meta:
        model = Subscriber
        read_only_fields = ('status',)


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

    def validate_timestamp(self, value: str):
        time = datetime.strptime(value, settings.DATETIME_FORMAT)
        if datetime.now(time.tzinfo) > time + timedelta(seconds=30):
            raise serializers.ValidationError(f'The request has expired. Max validity of any request is 30s')

 
class WriteSubscriberSerializer(serializers.Serializer):
    context = WriteSubscriberContextSerializer(required=True)
    message = WriteSubscriberMessageSerializer(required=True)

    
    def create(self, validated_data):
        subscriber = self.message.entity.create(**validated_data['message']['entity'])
        NetworkParticipant.objects.bulk_create(
            [NetworkParticipant(**participant.validated_data, subscriber=subscriber
                                ) for participant in self.message.network_participant]
        )
        return subscriber
        # TODO: Queue post processing





