poetry export -f requirements.txt -o requirements.txt --without-hashes
SET JWT_SECRET_KEY="secret"
SET ACCESS_TOKEN_EXPIRE_MINUTES=30
cd ..
space dev backend
