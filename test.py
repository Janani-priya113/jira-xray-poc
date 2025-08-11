import os

# Get secret from environment
secret_value = os.getenv("MY_SECRET")+"sasasasasasasasas"
versionName = os.getenv("versionName")
status = os.getenv("status")

print("Secret from Jenkins:", secret_value,versionName,status)
# Use the secret for API calls, DB connections, etc.
