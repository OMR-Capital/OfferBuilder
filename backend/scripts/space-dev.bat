poetry export -f requirements.txt -o requirements.txt --without-hashes
SET JWT_SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
SET ACCESS_TOKEN_EXPIRE_MINUTES=30
SET AGENTS_API_KEY=2f5f9952ea5002bb29eec5951579a85c042b86cd
cd ..
space dev backend
