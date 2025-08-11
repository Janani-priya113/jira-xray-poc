import os
from updatedXrayStatus import update_xray_test_status

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
jira_api_token = os.getenv("jira_api_token")

# TEST_EXEC_KEY = os.getenv("TEST_EXEC_KEY")
# PASS_TEST_KEY = os.getenv("PASS_TEST_KEY")
# FAIL_TEST_KEY = os.getenv("FAIL_TEST_KEY")
TEST_EXEC_KEY = "MTSD-24"
PASS_TEST_KEY = "MTSD-23"
FAIL_TEST_KEY = "MTSD-23"

def main():
    print("✅ Reading variables from Jenkins...")
    print(f"Xray Client ID: {xray_client_id}")
    print(f"Xray Client Secret: {xray_client_secret}")
    print(f"Project Key: {projectKey}")
    print(f"Issue Key: {issueKey}")
    print(f"Version Name: {versionName}")
    print(f"Details: {details}")
    print(f"Error Message: {errorMessage}")
    print(f"Status: {status}")
    print(f"Jira URL: {jira_url}")
    print(f"Jira API Token: {jira_api_token}")

    # Call the imported function (if needed)
    update_xray_test_status(
        client_id=xray_client_id,
        client_secret=xray_client_secret,
        test_exec_key=TEST_EXEC_KEY,
        pass_test_key=PASS_TEST_KEY,
        fail_test_key=FAIL_TEST_KEY,
        status=status,
        version_name=versionName,
        details=details
    )

if __name__ == "__main__":
    main()