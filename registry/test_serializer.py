from django.test import TestCase
from .serializers import *
import json
import pytest
from pathlib import Path
from django.conf import settings
from datetime import datetime



class TestWriteSubscriberSerializer(TestCase):
    serializer_class = WriteSubscriberSerializer

    def setUp(self) -> None:
        super().setUp()
        directory = Path(__file__).parent
        with open(Path.joinpath(directory, "fixtures/subscribe_request_passing.json"), "r") as file:
            self.subscribe_pass_fixtures = json.load(file)
        with open(Path.joinpath(directory, "fixtures/subscribe_request_fail.json"), "r") as file:
            self.subscribe_fail_fixtures = json.load(file)
        with open(Path.joinpath(directory, "fixtures/subscriber_update_passing.json"), "r") as file:
            self.subscriber_update_passing_fixtures = json.load(file)
    
    def test_ops_1_fail_request_expiry(self):
        fixture = list(filter(lambda fx: fx['context']['operation']['ops_no'] == 1, self.subscribe_pass_fixtures))[0]
        serialized  = self.serializer_class(data=fixture)
        with pytest.raises(serializers.ValidationError) as err:
            serialized.is_valid(raise_exception=True)
        exc = err.value.args[0]['message']['timestamp'][0]
        self.assertEqual(str(exc),'The request has expired. Max validity of any request is 30s')
    
    def test_ops_pass(self):
        for fixture in filter(lambda fx: fx['context']['operation']['ops_no'] == 1, self.subscribe_pass_fixtures):
            fixture['message']['timestamp'] = datetime.now()
            serialized  = self.serializer_class(data=fixture)
            self.assertTrue(serialized.is_valid(raise_exception=False))
    
    def test_ops_fail(self):
        for fixture in self.subscribe_fail_fixtures:
            fixture['message']['timestamp'] = datetime.now()
            serialized  = self.serializer_class(data=fixture)
            with pytest.raises(serializers.ValidationError) as err:
                serialized.is_valid(raise_exception=True)
            exc = err.value.args[0]['operation'][0]
            exp_str = ""
            match fixture['context']['operation']['ops_no']:
                case 1:
                    exp_str = "ops_no 1 can only create new BAP."
                case 2:
                    exp_str = "ops_no 2 can only create new Non-MSN BPP."
                case 3:
                    exp_str = "ops_no 3 can only create new MSN BPP."
                case 4:
                    exp_str = "ops_no 4 can only create BAP and Non-MSN BPP together."
                case 5:
                    exp_str = "ops_no 5 can only create BAP and MSN BPP together."
            self.assertEqual(str(exc), exp_str)