import logging
import sys

import requests
from decouple import config


HOST_BASE_URL = config("HOST_BASE_URL", None)
TELEGRAM_API_KEY = config("TELEGRAM_TOKEN", None)
