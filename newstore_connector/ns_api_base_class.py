"""
Parent class for the NewStore API Classes
"""

class NewStoreAPIBase:
    """
    Parent class for the NewStore API classes
    """

    def __init__(self, **kwargs) -> None:

        self.base_url = kwargs.get('base_url')
        self.session = kwargs.get('session')
        self.headers = kwargs.get('headers')
        