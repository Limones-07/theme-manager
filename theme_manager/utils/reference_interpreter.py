from .. import logging_utils

"""Provides a function to parse and replace references in a dictionary. """

_REFERENCE_TYPES = {'string': str, 'path': str, 'number': float, 'integer': int, 'float': float, 'boolean': bool}
_DEFAULT_REFERENCES = {'@THEME_DIR': 'path', '@HOME': 'path', '@SCRIPT': None}


