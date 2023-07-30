"""Project configuration.

For env variables see `Spacefile`.
"""

from os import environ

JWT_SECRET_KEY = environ['JWT_SECRET_KEY']

ACCESS_TOKEN_EXPIRE_MINUTES = int(environ['ACCESS_TOKEN_EXPIRE_MINUTES'])

AGENTS_API_KEY = environ['AGENTS_API_KEY']

PDF_API_KEY = environ['PDF_API_KEY']
