# Import the client from the config module
from .config import client
# Define what should be available when using 'from package import *'
__all__ = ['client']
__version__ = '0.1.0'
__author__ = 'OpenAI cli'
