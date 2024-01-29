"""
Module for defining the NewStoreConnector Class
"""

from api_toolkit.connector import APIConnector
from api_toolkit import modifiers as m

STATUS_FORCELIST = [408, 413, 429, 500, 502, 503, 504, 521, 522, 524]
BACKOFF_FACTOR = 2
class NewStoreConnector(APIConnector):
    """
    Primary class for interacting with the NewStore API
    """
    def __init__(self, **kwargs):
        """
        Initialize the NewStoreConnector Class
        """
        # Populate parameters and establish the connection
        self._validate_init_params(**kwargs)

        # Check if retry settings have been passed, if not, set defaults
        kwargs.setdefault("status_forcelist", STATUS_FORCELIST)
        kwargs.setdefault("backoff_factor", BACKOFF_FACTOR)

        # Initialize the APIConnector Class features
        super().__init__(**kwargs)

        # Set the tenant information for the NewStore API
        self.tenant = kwargs.get("tenant")
        self.env = kwargs.get("env", "p")
        self._base_url = f"https://{self.tenant}.{self.env}.newstore.net/"
        self.client_id = kwargs.get("client_id")
        self.client_secret = kwargs.get("client_secret")
        self.role = kwargs.get("role")

        # This needs to be done after super().__init__ because it uses the
        # session created in the parent class
        self.token_ttl = None # Used if This class fetches a Token
        self.roles = [] # Caching valid roles for client for potential future use
        self.token = kwargs.get("token") or self._get_auth_token()

        # Initialize empty instance variables for the API Classes
        self._order_injection = None
        self._order_notes = None

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

        payload = 'grant_type=client_credentials'
        payload += f'&scope={m.url_encode(self.role)}' if self.role else ''
        response = self.session.post(url, headers=headers, data=payload)
        response.raise_for_status()
        self.token_ttl = response.json().get("expires_in")
        self.roles = response.json().get("scope").split(" ")
        return response.json().get("access_token")

    def _get_headers(self):
        """
        Return the basic header for making NewStore API Requests
        """
        return {
            'Authorization': f'Bearer {self.token}'
        }

    @property
    def base_url(self):
        """
        Return the base URL for the NewStore API
        """
        return self._base_url

    # Define the API Classes as Properties Here
    # This allows us to only initialize the API Classes when they are needed
    # pylint: disable=import-outside-toplevel
    @property
    def order_injection(self):
        """
        Return the appropriate OrderInjection Class for the NewStore API
        """
        if not self._order_injection:
            self.order_injection = "0.1"

        return self._order_injection

    @order_injection.setter
    def order_injection(self, value):
        """
        Set the OrderInjection Class based on the version passed to the setter
        """
        if value == "0.1":
            from .order_injection import OrderInjectionV01

            self._order_injection = OrderInjectionV01()
            self._order_injection.headers = self._get_headers()
            self._order_injection.session = self.session
            self._order_injection.base_url = self.base_url
        else:
            raise ValueError(f"Invalid OrderInjection Version: {value}")

    @property
    def order_notes(self):
        """
        Return the appropriate OrderNotes Class for the NewStore API
        """
        if not self._order_notes:
            self.order_notes = "0.1.0"

        return self._order_notes

    @order_notes.setter
    def order_notes(self, value):
        """
        Set the OrderNotes Class based on the version passed to the setter
        """
        if value == "0.1.0":
            from .order_notes import OrderNotesV010

            self._order_notes = OrderNotesV010()
            self._order_notes.headers = self._get_headers()
            self._order_notes.session = self.session
            self._order_notes.base_url = self.base_url
        else:
            raise ValueError(f"Invalid OrderNotes Version: {value}")
