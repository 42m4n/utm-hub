import hashlib
import sys

# secret_salt
salt = sys.argv[1] 
# token_to_encode
token = sys.argv[2]

hashed_token = hashlib.sha256((salt + token).encode()).hexdigest()

print("Encoded Token:", hashed_token)

