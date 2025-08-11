# import os
# import requests
# import json


# def create_bug_ticket(jira_url, jira_email, jira_api_token, project_key, summary, description):
#     """Create a bug ticket in Jira."""
#     url = f"{jira_url}/rest/api/3/issue"
#     auth = (jira_email, jira_api_token)
#     headers = {
#         "Accept": "application/json",
#         "Content-Type": "application/json"
#     }

#     payload = {
#         "fields": {
#             "project": {"key": project_key},
#             "summary": summary,
#             "description": description,
#             "issuetype": {"name": "Bug"}
#         }
#     }

#     response = requests.post(url, auth=auth, headers=headers, json=payload)
#     if response.status_code == 201:
#         bug_key = response.json().get("key")
#         print(f"🐞 Bug created in Jira: {bug_key}")
#         return bug_key
#     else:
#         print(f"❌ Failed to create bug: {response.status_code} - {response.text}")
#         return None
    
# def update_xray_test_status(
#     client_id,
#     client_secret,
#     test_exec_key,
#     pass_test_key,
#     fail_test_key,
#     status,
#     version_name=None,
#     details=None
# ):
#     """
#     Authenticate with Xray, get Test Run ID, and update its status.
#     Falls back to REST API if GraphQL fails.
#     """

#     # 1️⃣ Authenticate with Xray to get token
#     auth_url = "https://xray.cloud.getxray.app/api/v1/authenticate"
#     auth_payload = {"client_id": client_id, "client_secret": client_secret}
#     auth_response = requests.post(auth_url, json=auth_payload)

#     if auth_response.status_code != 200:
#         raise Exception(f"Auth failed: {auth_response.status_code} - {auth_response.text}")

#     xray_token = auth_response.json().strip('"')
#     print("✅ Xray token obtained successfully")

#     # 2️⃣ Determine target test key & status
#     target_test_key = pass_test_key if status.upper() == "PASS" else fail_test_key
#     test_status = "PASSED" if status.upper() == "PASS" else "FAILED"
#     comment = (
#         f"Version {version_name} created successfully"
#         if status.upper() == "PASS"
#         else f"Version creation failed: {details or 'Unknown error'}"
#     )

#     # 3️⃣ Get Test Run ID via GraphQL
#     graphql_url = "https://xray.cloud.getxray.app/api/v2/graphql"
#     get_test_run_query = {
#         "query": f"""
#             query {{
#                 getTestRuns(testExecIssueIds: ["{test_exec_key}"], testIssueIds: ["{target_test_key}"], limit: 10) {{
#                     results {{
#                         id
#                         testType {{ name }}
#                     }}
#                 }}
#             }}
#         """
#     }
#     headers = {
#         "Authorization": f"Bearer {xray_token}",
#         "Content-Type": "application/json"
#     }

#     tr_response = requests.post(graphql_url, headers=headers, json=get_test_run_query)

#     test_run_id = None
#     if tr_response.status_code == 200:
#         tr_data = tr_response.json()
#         if "errors" not in tr_data and tr_data.get("data", {}).get("getTestRuns", {}).get("results"):
#             test_run_id = tr_data["data"]["getTestRuns"]["results"][0]["id"]
#             print(f"✅ Test run ID found: {test_run_id}")
#         else:
#             print("⚠️ No test runs found in response")
#     else:
#         print(f"❌ GraphQL query failed: {tr_response.status_code} - {tr_response.text}")

#     # 4️⃣ Update test status
#     if test_run_id:
#         # Use GraphQL mutation
#         mutation_query = {
#             "query": f"""
#                 mutation {{
#                     updateTestRunStatus(id: "{test_run_id}", status: "{test_status}")
#                 }}
#             """
#         }
#         update_response = requests.post(graphql_url, headers=headers, json=mutation_query)
#         if update_response.status_code == 200 and "errors" not in update_response.json():
#             print(f"✅ Test {target_test_key} status updated to {test_status} (GraphQL)")
#         else:
#             print(f"❌ GraphQL update failed: {update_response.text}")
#     else:
#         # Fallback to REST API
#         print("🔄 Using REST API fallback to update test status")
#         rest_url = "https://xray.cloud.getxray.app/api/v1/import/execution"
#         rest_payload = {
#             "testExecutionKey": test_exec_key,
#             "tests": [
#                 {
#                     "testKey": target_test_key,
#                     "status": test_status,
#                     "comment": comment
#                 }
#             ]
#         }
#         rest_response = requests.post(rest_url, headers=headers, json=rest_payload)
#         if rest_response.status_code == 200:
#             print(f"✅ Test {target_test_key} status updated via REST API")
#         else:
#             print(f"❌ REST API update failed: {rest_response.status_code} - {rest_response.text}")


import os
import requests
import json

def create_bug_ticket(jira_url, jira_email, jira_api_token, project_key, summary, description):
    """Create a bug ticket in Jira."""
    url = f"{jira_url}/rest/api/3/issue"
    auth = (jira_email, jira_api_token)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = {
        "fields": {
            "project": {"key": project_key},
            "summary": summary,
            "description": description,
            "issuetype": {"name": "Bug"}
        }
    }

    response = requests.post(url, auth=auth, headers=headers, json=payload)
    if response.status_code == 201:
        bug_key = response.json().get("key")
        print(f"🐞 Bug created in Jira: {bug_key}")
        return bug_key
    else:
        print(f"❌ Failed to create bug: {response.status_code} - {response.text}")
        return None


def update_xray_test_status(
    client_id,
    client_secret,
    test_exec_key,
    pass_test_key,
    fail_test_key,
    status,
    version_name=None,
    details=None,
    jira_url=None,
    jira_email=None,
    jira_api_token=None,
    jira_project_key=None
):
    """Authenticate with Xray, get Test Run ID, and update its status.
       Falls back to REST API if GraphQL fails. If both fail, creates a bug ticket.
    """

    # 1️⃣ Authenticate with Xray to get token
    auth_url = "https://xray.cloud.getxray.app/api/v1/authenticate"
    auth_payload = {"client_id": client_id, "client_secret": client_secret}
    auth_response = requests.post(auth_url, json=auth_payload)

    if auth_response.status_code != 200:
        raise Exception(f"Auth failed: {auth_response.status_code} - {auth_response.text}")

    xray_token = auth_response.json().strip('"')
    print("✅ Xray token obtained successfully")

    # 2️⃣ Determine target test key & status
    target_test_key = pass_test_key if status.upper() == "PASS" else fail_test_key
    test_status = "PASSED" if status.upper() == "PASS" else "FAILED"
    comment = (
        f"Version {version_name} created successfully"
        if status.upper() == "PASS"
        else f"Version creation failed: {details or 'Unknown error'}"
    )

    # 3️⃣ Get Test Run ID via GraphQL
    graphql_url = "https://xray.cloud.getxray.app/api/v2/graphql"
    get_test_run_query = {
        "query": f"""
            query {{
                getTestRuns(testExecIssueIds: ["{test_exec_key}"], testIssueIds: ["{target_test_key}"], limit: 10) {{
                    results {{
                        id
                        testType {{ name }}
                    }}
                }}
            }}
        """
    }
    headers = {
        "Authorization": f"Bearer {xray_token}",
        "Content-Type": "application/json"
    }

    tr_response = requests.post(graphql_url, headers=headers, json=get_test_run_query)

    test_run_id = None
    if tr_response.status_code == 200:
        tr_data = tr_response.json()
        if "errors" not in tr_data and tr_data.get("data", {}).get("getTestRuns", {}).get("results"):
            test_run_id = tr_data["data"]["getTestRuns"]["results"][0]["id"]
            print(f"✅ Test run ID found: {test_run_id}")
        else:
            print("⚠️ No test runs found in response")
    else:
        print(f"❌ GraphQL query failed: {tr_response.status_code} - {tr_response.text}")

    # 4️⃣ Update test status
    update_success = False
    if test_run_id:
        mutation_query = {
            "query": f"""
                mutation {{
                    updateTestRunStatus(id: "{test_run_id}", status: "{test_status}")
                }}
            """
        }
        update_response = requests.post(graphql_url, headers=headers, json=mutation_query)
        if update_response.status_code == 200 and "errors" not in update_response.json():
            print(f"✅ Test {target_test_key} status updated to {test_status} (GraphQL)")
            update_success = True
        else:
            print(f"❌ GraphQL update failed: {update_response.text}")

    if not update_success:
        print("🔄 Using REST API fallback to update test status")
        rest_url = "https://xray.cloud.getxray.app/api/v1/import/execution"
        rest_payload = {
            "testExecutionKey": test_exec_key,
            "tests": [
                {
                    "testKey": target_test_key,
                    "status": test_status,
                    "comment": comment
                }
            ]
        }
        rest_response = requests.post(rest_url, headers=headers, json=rest_payload)
        if rest_response.status_code == 200:
            print(f"✅ Test {target_test_key} status updated via REST API")
            update_success = True
        else:
            print(f"❌ REST API update failed: {rest_response.status_code} - {rest_response.text}")

    # 5️⃣ If still failed, create a bug ticket
    print("🔄 Checking if Jira bug ticket needs to be created...")
    if not update_success and jira_url and jira_email and jira_api_token and jira_project_key:
        print("🚨 Both GraphQL and REST failed. Creating Jira Bug ticket...")
        summary = f"Failed to update Xray test status for {target_test_key}"
        description = f"Attempted to update status to {test_status} but both GraphQL and REST API failed.\nDetails: {details}"
        create_bug_ticket(jira_url, jira_email, jira_api_token, jira_project_key, summary, description)
