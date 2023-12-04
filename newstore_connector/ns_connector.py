"""
Module for defining the NewStoreConnector Class
"""

from api_toolkit.connector import APIConnector
from api_toolkit import modifiers as m


class NewStoreConnector(APIConnector):
    """
    Primary class for interacting with the NewStore API
    """
    def __init__(self, **kwargs):
        """
        Initialize the NewStoreConnector Class
        """
        self._validate_init_params(**kwargs)
        # Initialize the APIConnector Class features
        super().__init__(**kwargs)
        # Set the tenant information for the NewStore API
        self.tenant = kwargs.get("tenant")
        self.env = kwargs.get("enc", "p")
        self._base_url = f"https://{self.tenant}.{self.env}.newstore.net/"
        self.client_id = kwargs.get("client_id")
        self.client_secret = kwargs.get("client_secret")
        self.role = kwargs.get("role", "iam:providers:read")
        self.token = kwargs.get("token", self._get_auth_token())

    def _validate_init_params(self, **kwargs):
        """
        Validate the required parameters are present and raise an exception
        If they are not
        """
        error_dict = {}
        # If tenant is not provided
        if not kwargs.get("tenant"):
            error_dict["tenant"] = "Missing required parameter"
        # If client_id is provided but client_secret and token are not
        if kwargs.get('client_id') and\
              not kwargs.get('client_secret') and\
                  not kwargs.get('token'):
            error_dict["client_secret"] = "client_secret required for client_id authentication"
        # If client_secret is provided but client_id and token are not
        if kwargs.get('client_secret') and\
              not kwargs.get('client_id') and\
                  not kwargs.get('token'):
            error_dict["client_id"] = "client_id required for client_id authentication"
        # If token, client_id, and client_secret are not provided
        if not kwargs.get('token') and\
              not kwargs.get('client_id') and\
                  not kwargs.get('client_secret'):
            error_dict["Auth"] = "client_id/client_secret or Token required for authentication"
        # If there are errors, raise ValueError
        if error_dict:
            raise ValueError(error_dict)

    def _get_auth_token(self):
        """
        Get the authentication token for the NewStore API
        """
        url = f"https://id.p.newstore.net/auth/realms/{self.tenant}/protocol/openid-connect/token"

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Basic {m.base64_encode(f"{self.client_id}:{self.client_secret}")}'
        }

        payload = f'grant_type=client_credentials&scope={m.url_encode(self.role)}'
        response = self.session.post(url, headers=headers, data=payload)
        response.raise_for_status()
        return response.json().get("access_token")

    @property
    def base_url(self):
        """
        Return the base URL for the NewStore API
        """
        return self._base_url
