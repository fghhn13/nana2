import pytest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

try:
    import requests
except ImportError:  # pragma: no cover - network library optional
    requests = None

from global_config.settings import Api_url


def test_api_connection():
    if requests is None:
        pytest.skip("requests library not installed")
    api_url = Api_url
    try:
        response = requests.head(api_url, timeout=15)
        assert response.status_code < 500
    except requests.exceptions.RequestException as e:  # pragma: no cover - network errors
        pytest.fail(f"connection failed: {e}")
