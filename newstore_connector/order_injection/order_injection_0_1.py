"""
Module for connecting to NewStore Order Injection API v0.1
https://docs.newstore.net/api/integration/order-management/order_injection_api
"""

from api_toolkit.validate import RuleSet
from api_toolkit.validate import Rules as r
from api_toolkit.connector.decorators import json_or_full

from ..request_lists import CURRENCY_LIST

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

        # Validate the payload if not skipped
        if kwargs.get('skip_validation') is True:
            rule_set = self._create_order_validation_ruleset()
            rule_set.test_dict = payload

            if not rule_set:
                raise ValueError(rule_set.errors)

        response = self.session.post(url,
                                     headers=self.headers or kwargs.get('headers'),
                                     json=payload)
        response.raise_for_status()

        return response

    def _create_order_validation_ruleset(self):
        """
        Build and return the validation dictionary for the create_order API
        """
        # Define Parent Validation Ruleset
        validation_dict = {
            'external_id': [r.required(), r.is_type(str), r.length(min=1, max=64)],
            'shop': [r.required(), r.is_type(str), r.length(min=1, max=128)],
            'channel_type': [r.required(), r.is_type(str), r.is_in('web', 'mobile', 'store')],
            'channel_name': [r.required(), r.is_type(str), r.length(min=1, max=64)],
            'store_id': [r.is_type(str), r.length(max=256)],
            'associate_id': [r.is_type(str), r.length(max=256)],
            'customer_name': [r.is_type(str), r.length(max=128)],
            'customer_email': [r.is_type(str), r.email(), r.length(max=64)],
            'shop_locale': [r.required(), r.is_type(str), r.length(min=1, max=128)],
            'customer_language': [r.is_type(str), r.length(max=2)],
            'external_customer_id': [r.is_type(str), r.length(max=64)],
            'placed_at': [r.is_type(str)],
            'ip_address': [r.is_type(str)],
            'shipping_address': [r.is_type(dict), self._build_address_validation_ruleset()],
            'shipments': [r.required(),
                          r.is_type(list),
                          [self._build_shipment_validation_ruleset()]
                         ],
            'extended_attributes': [r.is_type(list),
                                    [self._build_extended_attributes_validation_ruleset()]],
            'billing_address': [r.is_type(dict), self._build_address_validation_ruleset()],
            'payments': [r.is_type(list), [self._build_payment_validation_dict()]],
            'price_method': [r.is_type(str), r.is_in('tax_included', 'tax_excluded')],
            'is_preconfirmed': [r.is_type(bool)],
            'is_fulfilled': [r.is_type(bool)],
            'is_offline': [r.is_type(bool)],
            'is_historical': [r.is_type(bool)],
            'notification_blacklist': [r.is_type(list), [r.is_type(str)]],
            'currency': [r.required(), r.is_type(str), r.is_in(*CURRENCY_LIST)]
        }
        order_validation_ruleset = RuleSet(validation_dict)
        return order_validation_ruleset

    def _build_address_validation_ruleset(self):
        """
        Build the validation ruleset for address validation
        """
        # Define the ruleset for the address validation
        str_32_char = [r.is_type(str), r.length(max=32)]
        str_64_char = [r.is_type(str), r.length(max=64)]
        address_validation_dict = {
            'title': str_32_char,
            'suffix': str_32_char,
            'salutation': str_32_char,
            'first_name': str_64_char,
            'last_name': str_64_char,
            'country': [r.required(), r.is_type(str), r.length(min=2, max=2)],
            'zip_code': str_32_char,
            'city': str_64_char,
            'state': str_32_char,
            'address_line_1': [r.required(), r.is_type(str), r.length()],
            'address_line_2': [r.is_type(str), r.length(max=256)],
            'phone': [r.is_type(str), r.length(max=128)]
        }
        address_rule_set = RuleSet(address_validation_dict)

        return address_rule_set

    def _build_shipment_validation_ruleset(self):
        """
        Build the shipment validation ruleset for create_order API
        """
        # Define Shipments Validation Ruleset
        shipment_validation = {
            'items': [r.required(),
                      r.is_type(list),
                      [r.is_type(dict),
                       self._build_item_validation_ruleset()]
                    ],
            'shipping_option': [r.required(), self._build_shipping_option_validation_ruleset()],
        }
        shipment_ruleset = RuleSet(shipment_validation)
        return shipment_ruleset

    def _build_item_validation_ruleset(self):
        """
        Build the item validation ruleset for create_order API
        """
        # Define Item Validation Dict
        item_validation_dict = {
            'external_item_id': [r.required(), r.is_type(str), r.length(min=1, max=64)],
            'product_id': [r.required(), r.is_type(str), r.length(min=1, max=64)],
            'price': [r.required(), r.is_type(dict), self._build_price_validation_ruleset()],
            'gift_wrapping': [r.is_type(bool)],
            'extended_attributes': [r.is_type(list),
                                    [self._build_extended_attributes_validation_ruleset()]
                                   ]
        }

        item_validation_ruleset = RuleSet(item_validation_dict)
        return item_validation_ruleset

    def _build_price_validation_ruleset(self):
        """
        Build the price validation ruleset used in the item validation ruleset
        """
        # Define Price Validation Dict
        price_validation_dict = {
            'item_price': [r.required(), r.is_type(int, float)],
            'item_list_price': [r.required(), r.is_type(int, float)],
            'item_tax_lines': [r.required(),
                               r.is_type(list),
                               [self._build_item_tax_lines_validation_ruleset()]
                              ],
            'item_order_discount_info': [r.is_type(list),
                                         [self._build_order_discount_validation_ruleset()]],
            'pricebook': [r.is_type(str), r.length(max=64)],
            'group_ref': [r.is_type(str), r.length(max=64)]
        }

        price_validation_ruleset = RuleSet(price_validation_dict)
        return price_validation_ruleset

    def _build_order_discount_validation_ruleset(self):
        """
        Build the order discount validation ruleset used in the price validation ruleset
        """
        # Define Order Discount Validation Dict
        order_discount_validation_dict = {
            'discount_ref': [r.required(), r.is_type(str), r.length(max=256)],
            'coupon_code': [r.is_type(str), r.length(max=64)],
            'description': [r.is_type(str), r.length(max=1024)],
            'type': [r.required(), r.is_type(str), r.is_in('fixed')],
            'original_value': [r.required(), r.is_type(int, float), r.Min(0)],
            'price_adjustment': [r.required(), r.is_type(int, float), r.Min(0)]
        }
        order_discount_validation_ruleset = RuleSet(order_discount_validation_dict)
        return order_discount_validation_ruleset

    def _build_item_tax_lines_validation_ruleset(self):
        """
        Build the tax lines validation ruleset used in the price validation ruleset
        """
        # Define Item Tax Lines Validation Dict
        item_tax_lines_validation_dict = {
            'amount': [r.required(), r.is_type(int, float)],
            'rate': [r.required(), r.is_type(float), r.Min(0), r.Max(1)],
            'name': [r.required(), r.is_type(str)],
            'country_code': [r.is_type(str), r.length(max=2)]
        }
        item_tax_lines_validation_ruleset = RuleSet(item_tax_lines_validation_dict)
        return item_tax_lines_validation_ruleset

    def _build_extended_attributes_validation_ruleset(self):
        """
        Build the validation ruleset for extended attributes
        """
        # Define Extended Attributes Validation Dict
        extended_attributes_validation_dict = {
            'name': [r.required(), r.is_type(str), r.length(min=1, max=100)],
            'value': [r.required(), r.is_type(str), r.length(max=8192)]
        }
        extended_attributes_validation_ruleset = RuleSet(extended_attributes_validation_dict)
        return extended_attributes_validation_ruleset

    def _build_shipping_option_validation_ruleset(self):
        """
        Build the validation ruleset for shippiing option validation
        """
        # Define Shipping Options Validation Dict
        shipping_options_validation_dict = {
            'service_level_identifier': [r.required(), r.is_type(str), r.length(min=1, max=64)],
            'price': [r.required(), r.is_type(int, float), r.Min(0)],
            'tax': [r.required(), r.is_type(int, float), r.Min(0)],
            'discount_info': [r.is_type(list), self._build_order_discount_validation_ruleset()],
            'routing_strategy': [r.is_type(dict), self._build_routing_strategy_validation_ruleset()]
        }
        shipping_options_validation_ruleset = RuleSet(shipping_options_validation_dict)
        return shipping_options_validation_ruleset

    def _build_routing_strategy_validation_ruleset(self):
        """
        Build the validation ruleset for routing strategy validation
        """
        # Define Routing Strategy Validation Dict
        routing_strategy_validation_dict = {
            'strategy': [r.required(), r.is_type(str)]
        }
        routing_strategy_validation_ruleset = RuleSet(routing_strategy_validation_dict)
        return routing_strategy_validation_ruleset

    def _build_payment_validation_dict(self):
        """
        Build the payment validation ruleset for order validation
        """
        # Define Payment Validation Dict
        payment_validation_dict = {
            'type': [r.required(), r.is_type(str), r.is_in('authorized', 'captured')],
            'amount': [r.required(), r.is_type(int, float), r.Min(0.01)],
            'method': [r.required(), r.is_type(str), r.length(min=1, max=64)],
            'wallet': [r.is_type(str), r.length(min=1,max=64)],
            'processed_at': [r.required(), r.is_type(str)],
            'metadata': [r.is_type(dict), r.length(max=100)],
            'processor': [r.required(), r.is_type(str), r.length(min=1, max=32)],
            'correlation_ref': [r.required(), r.is_type(str), r.length(min=1, max=128)]
        }
        payment_validation_ruleset = RuleSet(payment_validation_dict)
        return payment_validation_ruleset
