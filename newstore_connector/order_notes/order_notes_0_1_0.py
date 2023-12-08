"""
Module for connecting to the NewStore Order Notes API
https://docs.newstore.net/api/integration/order-management/order_notes_api
"""

from api_toolkit.connector.decorators import json_or_full

from ..ns_api_base_class import NewStoreAPIBase


class OrderNotesV010(NewStoreAPIBase):
    """
    Class for interacting with the NewStore Order Notres API
    """
    api_version = "0.1.0"

    @json_or_full
    def get_order_notes(self, order_uuid):
        """
        Get the notes for a specific order
        https://docs.newstore.net/api/integration/order-management/order_notes_api#operation/showOrderNote
        """
        endpoint = f"/v0/d/orders/{order_uuid}/notes"
        url = self.base_url + endpoint
        response = self.session.get(url, headers=self.headers, timeout=30)
        response.raise_for_status()

        return response

    @json_or_full
    def create_order_note(self, order_uuid, **kwargs):
        """
        Create an order note
        Args:
            order_uuid(str): The UUID of the order
            text(str): The text of the note
            source(str): The user_id of the user creating the note
            source_type(str): The type of the source defaults to "integration"
            tags(list): A list of tags to apply to the note
        For More Information:
        https://docs.newstore.net/api/integration/order-management/order_notes_api#operation/createOrderLevelNote
        """
        endpoint = f"/v0/d/orders/{order_uuid}/notes"
        url = self.base_url + endpoint

        payload = {
            "text": kwargs.get("text"),
            "source": kwargs.get("source"),
            "source_type": kwargs.get("source_type", "integration"),
            "tags": kwargs.get("tags")
        }

        response = self.session.post(url, headers=self.headers, json=payload, timeout=30)
        response.raise_for_status()

        return response

    def create_item_note(self, order_uuid, item_uuid, **kwargs):
        """
        Create a note for an item
        Args:
            order_uuid(str): The UUID of the order
            item_uuid(str): The UUID of the item
            text(str): The text of the note
            source(str): The user_id of the user creating the note
            source_type(str): The type of the source defaults to "integration"
            tags(list): A list of tags to apply to the note
        For More Information:
        https://docs.newstore.net/api/integration/order-management/order_notes_api#operation/createItemLevelNote
        """
        endpoint = f"/v0/d/orders/{order_uuid}/items/{item_uuid}/notes"
        url = self.base_url + endpoint

        payload = {
            "test": kwargs.get("text"),
            "source": kwargs.get("source"),
            "source_type": kwargs.get("source_type", "integration"),
            "tags": kwargs.get("tags")
        }

        response = self.session.post(url, headers=self.headers, json=payload, timeout=30)
        response.raise_for_status()

        return response

    def update_note(self, order_uuid, note_uuid, **kwargs):
        """
        Runs PATCH update for notes API
        Args:
            order_uuid(str): The UUID of the order
            note_uuid(str): The UUID of the note
            text(str): The text of the note
            source(str): The user_id of the user creating the note
            source_type(str): The type of the source defaults to "integration"
            tags(list): A list of tags to apply to the note
        For More Information:
        https://docs.newstore.net/api/integration/order-management/order_notes_api#operation/updateNote
        """
        endpoint = f"/v0/d/orders/{order_uuid}/notes/{note_uuid}"
        url = self.base_url + endpoint

        payload = {
            "text": kwargs.get("text"),
            "source": kwargs.get("source"),
            "source_type": kwargs.get("source_type", "integration"),
            "tags": kwargs.get("tags")
        }

        response = self.session.patch(url, headers=self.headers, json=payload, timeout=30)
        response.raise_for_status()

        return response

    def delete_note(self, order_uuid, note_uuid):
        """
        Delete a note
        Args:
            order_uuid(str): The UUID of the order
            note_uuid(str): The UUID of the note
        For More Information:
        https://docs.newstore.net/api/integration/order-management/order_notes_api#operation/destroyNote
        """
        endpoint = f"/v0/d/orders/{order_uuid}/notes/{note_uuid}"
        url = self.base_url + endpoint

        response = self.session.delete(url, headers=self.headers, timeout=30)
        response.raise_for_status()

        return response
