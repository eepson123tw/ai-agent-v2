# Import the client from the config module
from .config import client
from .message_db import init_message, add_message, get_messages
# Define what should be available when using 'from package import *'
__all__ = ['client','init_message', 'add_message', 'get_messages']
__version__ = '0.1.0'
__author__ = 'OpenAI cli'
