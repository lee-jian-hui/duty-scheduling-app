from __future__ import annotations

import os
from dataclasses import dataclass
from enum import Enum
from typing import List


class Environment(str, Enum):
    development = "development"
    production = "production"
    test = "test"


class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


DEV_FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
PROD_FRONTEND_ORIGIN = os.getenv("PROD_FRONTEND_ORIGIN", "http://localhost:4173")
