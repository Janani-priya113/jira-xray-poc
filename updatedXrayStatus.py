import os
import requests
import json

def update_xray_test_status(
    client_id,
    client_secret,
    test_exec_key,
    pass_test_key,
    fail_test_key,
    status,
    version_name=None,
    details=None
):
    """
    Authenticate with Xray, get Test Run ID, and update its status.
    Falls back to REST API if GraphQL fails.
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
    if test_run_id:
        # Use GraphQL mutation
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
        else:
            print(f"❌ GraphQL update failed: {update_response.text}")
    else:
        # Fallback to REST API
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
        else:
            print(f"❌ REST API update failed: {rest_response.status_code} - {rest_response.text}")
