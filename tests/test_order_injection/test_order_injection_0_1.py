"""
Test Order Injection V01
"""
import os
import json
from newstore_connector.order_injection import OrderInjectionV01


def test_order_payload_validation_valid_order():
    """
    Test that the order_payload_validation will accurately validate the payload
    """

    # Open ./fixtures/valid_order_payload.json
    fixtures_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures')
    with open(os.path.join(fixtures_path,"valid_order_payload.json"),
              "r", encoding='utf-8') as file:
        valid_payload = json.load(file)

    order_injection = OrderInjectionV01()

    validation_result = order_injection.validate_create_order_payload(valid_payload)

    assert bool(validation_result)
    assert not validation_result.errors


def test_order_payload_validation_invalid_order():
    """
    Test that order validation will work with an invalid order
    """
    # Open ./fixtures/invalid_order_payload.json
    fixtures_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures')

    with open(os.path.join(fixtures_path, "invalid_order_payload.json"),
              "r", encoding='utf-8') as file:
        invalid_payload = json.load(file)

    order_injection = OrderInjectionV01()

    validation_result = order_injection.validate_create_order_payload(invalid_payload)

    assert not bool(validation_result)
    assert len(validation_result.errors) == 1
