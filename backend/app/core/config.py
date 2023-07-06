"""Project configuration.

For env variables see `Spacefile`.
"""

from os import environ

JWT_SECRET_KEY = environ['JWT_SECRET_KEY']

ACCESS_TOKEN_EXPIRE_MINUTES = int(environ['ACCESS_TOKEN_EXPIRE_MINUTES'])
