from .models import * 
from rest_framework import serializers



class SellerOnRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = SellerOnRecord
        exclude = ('network_participant',)

class NetworkParticipantSerializer(serializers.ModelSerializer):
    seller_on_record = serializers.RelatedField(many=True)

    class Meta:
        model = NetworkParticipant
        exclude = ('subscriber',)

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


class WriteSubscriberOperationNumberSerializer(serializers.Serializer):
    ops_no = serializers.IntegerField(
        required=True,
        min_value=1,
        max_value=10
    )

class WriteSubscriberContextSerializer(serializers.Serializer):
    operation = WriteSubscriberOperationNumberSerializer(required=True)

class WriteSubscriberMessageSerializer(serializers.Serializer):
    request_id = serializers.CharField(required=True)
    timestamp = serializers.DateTimeField(required=True)
    entity = SubscriberSerializer(required=True)
    network_participant = serializers.ListField(child=NetworkParticipantSerializer(), required=True)

class WriteSubscriberSerializer(serializers.Serializer):
    context = WriteSubscriberContextSerializer(required=True)
    message = WriteSubscriberMessageSerializer(required=True)


