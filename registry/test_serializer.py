from django.test import TestCase
from .serializers import *
import json
import pytest
from pathlib import Path
from django.conf import settings
from datetime import datetime


@pytest.fixture
def subscribe_create_fixtures():
    directory = Path(__file__).parent
    return json.load(open(Path.joinpath(directory, "fixtures/subscribe_create_request.json"), "r"))

@pytest.fixture
def ops_1_create_fixtures(subscribe_create_fixtures):
    return list(filter(lambda fx: fx['context']['operation']['ops_no'] == 1, subscribe_create_fixtures))



class TestWriteSubscriberSerializer(TestCase):
    serializer_class = WriteSubscriberSerializer

    def setUp(self) -> None:
        super().setUp()
        directory = Path(__file__).parent
        file = open(Path.joinpath(directory, "fixtures/subscribe_create_request.json"), "r")
        self.fixtures = json.load(file)
    
    def test_ops_1_fail_request_expiry(self):
        fixture = list(filter(lambda fx: fx['context']['operation']['ops_no'] == 1, self.fixtures))[0]
        serialized  = self.serializer_class(data=fixture)
        with pytest.raises(serializers.ValidationError) as err:
            serialized.is_valid(raise_exception=True)
        exc = err.value.args[0]['message']['timestamp'][0]
        self.assertEqual(str(exc),'The request has expired. Max validity of any request is 30s')
    
    def test_ops_1_pass(self):
        fixture = list(filter(lambda fx: fx['context']['operation']['ops_no'] == 1, self.fixtures))[0]
        fixture['message']['timestamp'] = datetime.now()
        serialized  = self.serializer_class(data=fixture)
        self.assertTrue(serialized.is_valid(raise_exception=True))