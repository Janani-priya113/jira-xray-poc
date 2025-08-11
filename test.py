import os

# Get secret from environment
secret_value = os.getenv("MY_SECRET")+"sasasasasasasasas"

print("Secret from Jenkins:", secret_value)
# Use the secret for API calls, DB connections, etc.
