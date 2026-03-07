"""Shared utilities for B2B skills."""

# Use absolute imports for pytest compatibility
try:
    from .brightdata_utils import get_api_key, LOCATION_MAP, create_client
    __all__ = ["get_api_key", "LOCATION_MAP", "create_client"]
except ImportError:
    # When running as standalone scripts
    from brightdata_utils import get_api_key, LOCATION_MAP, create_client
    __all__ = ["get_api_key", "LOCATION_MAP", "create_client"]
