import os

# Get secret from environment
xray_client_id = os.getenv("xray_client_id")
xray_client_secret = os.getenv("xray_client_secret")

projectKey = os.getenv("projectKey")
issueKey = os.getenv("issueKey")
versionName = os.getenv("versionName")
details = os.getenv("details")
errorMessage = os.getenv("errorMessage")
status = os.getenv("status")


print("Xray Client ID:", xray_client_id)
print("Xray Client Secret:", xray_client_secret)
print("Project Key:", projectKey)
print("Issue Key:", issueKey)
print("Version Name:", versionName)
print("Details:", details)
print("Error Message:", errorMessage)
print("Status:", status)

# Use the secret for API calls, DB connections, etc.
