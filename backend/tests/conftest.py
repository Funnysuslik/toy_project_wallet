import sys
import os
from pathlib import Path

import pytest
from faker import Faker
from datetime import datetime


backend_dir = Path(__file__).parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))


@pytest.fixture(scope="session")
def faker():
    return Faker()


@pytest.fixture
def now():
    return datetime.now(datetime.timezone.utc)
