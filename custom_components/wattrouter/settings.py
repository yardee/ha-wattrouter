from dataclasses import dataclass


@dataclass
class WattrouterSettings:
    """Class to manage component settings."""

    def __init__(
        self,
        username: str,
        password: str,
        url: str,
    ) -> None:
        """Initialize."""
        self.username = username
        self.password = password
        self.url = url
