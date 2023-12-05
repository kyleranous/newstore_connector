"""
Module for connecting to NewStore Order Injection API v0.1
https://docs.newstore.net/api/integration/order-management/order_injection_api
"""

from api_toolkit.validate import RuleSet
from api_toolkit.validate import Rules as r
from api_toolkit.connector.decorators import json_or_full


class OrderInjectionV01:
    """
    Class for handling Order Injection API requests
    """
    api_version = "0.1"

    def __init__(self, **kwargs):
        """
        Initialize the OrderInjection Class
        Expected kwargs:
        - token: The authentication token for the NewStore API
        - session: The requests Session object to use for requests
        - base_url: The base url for the NewStore API
        """
        self.headers = kwargs.get("headers") # Token would be passed in the headers
        self.session = kwargs.get("session")
        self.base_url = kwargs.get("base_url")

    @json_or_full
    def create_order(self, **kwargs):
        """
        Create Order API
        https://docs.newstore.net/api/integration/order-management/order_injection_api/#operation/CreateOrder
        """
        # Define paramters for the create_order API
        endpoint = '/v0/d/fulfill_order'
        url = f"{self.base_url or kwargs.get('base_url')}{endpoint}"
        payload = kwargs.get("payload")

        # Define the validation rules for the create_order API
        rule_set = RuleSet(self._create_order_validation(), test_dict=payload)

        if not rule_set:
            raise ValueError(rule_set.errors)

        response = self.session.post(url,
                                     headers=self.headers or kwargs.get('headers'),
                                     json=payload)
        response.raise_for_status()

        return response

    def _create_order_validation(self):
        """
        Build and return the validation dictionary for the create_order API
        """
        validation_dict = {
            'test': [r.is_type(str)]
        }

        return validation_dict
