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

jira_url = os.getenv("jira_url")
jira_api_token = os.getenv("jira_auth_token")


# print("Xray Client ID:", xray_client_id)
# print("Xray Client Secret:", xray_client_secret)
# print("Project Key:", projectKey)
# print("Issue Key:", issueKey)
# print("Version Name:", versionName)
# print("Details:", details)
# print("Error Message:", errorMessage)
# print("Status:", status)
print("Jira URL:", jira_url)
print("Jira API Token:", jira_api_token)

# Use the secret for API calls, DB connections, etc.
