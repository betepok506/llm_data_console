# conftest.py

import pytest
from unittest.mock import MagicMock

@pytest.fixture
def mocked_model():
    model = MagicMock()
    model.generate_code.side_effect = lambda q: MOCK_RESPONSES[q]
    return model