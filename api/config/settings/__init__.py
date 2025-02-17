"""
Django Settings Module
This module determines which settings file to use based on the environment.
"""
from .base import *

try:
    from .local import *
except ImportError:
    from .production import *
