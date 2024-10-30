import requests as r
import json


def create_netlify_site(access_token, subdomain):
    url = "https://api.netlify.com/api/v1/sites"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "name": f"blackksheepp-main.{subdomain}",
        "custom_domain": f"{subdomain}.mauito.com",
        "repo": {
            "provider": "github",
            "repo_path": "blackksheepp/web-auto-template",
            "repo_branch": "main",
            "cmd": "npm install && npm run start",
            "dir": "dist",
            "private": False,
            "allowed_branches": ["main"],
            "base": ".",
            "installation_id": 56525149,
        },
    }
    response = r.post(url, headers=headers, data=json.dumps(payload))
    return response.json()


def set_env_var(account_id, site_id, access_token, env_vars):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    for key, value in env_vars:
        url = f"https://api.netlify.com/api/v1/accounts/{account_id}/env/{key}?site_id={site_id}&context=production"

        body = {
            "key": key,
            "value": value,
            "scopes": ["builds"],
            "values": [{"context": "production"}],
            "is_secret": False,
        }
        response = r.patch(url, headers=headers, json=body)

    return response.json()


def retry_latest_deploy(site_id, access_token):
    get_url = f"https://api.netlify.com/api/v1/sites/{site_id}/deploys?page=1&per_page=1&branch=main"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    response = r.get(get_url, headers=headers)

    if response.status_code < 400:
        data = response.json()
        deploy_id = data[0]["id"] if data else None
    else:
        return {"error": response.status_code, "message": response.text}

    if deploy_id:
        retry_url = f"https://api.netlify.com/api/v1/deploys/{deploy_id}/retry"
        retry_response = r.post(retry_url, headers=headers, json={})

        if retry_response.status_code < 400:
            return {"success": True, "deploy_id": deploy_id}
        else:
            return {"error": retry_response.status_code, "message": retry_response.text}
    else:
        return {"error": "No deploys found for the specified site and branch."}


access_token = ""
account_id = ""

# Extracted from zapier
name = inputData["name"]
email = inputData["email"]
phone = inputData["phone"]
address = inputData["address"]
logo = inputData["logo"]
color = inputData["color"]
image = inputData["image"]

subdomain = inputData["subdomain"]

site_response = create_netlify_site(access_token, subdomain)
print(site_response)
if "id" in site_response.keys():
    site_id = site_response["id"]
    site_url = site_response["url"]

    output = {"url": site_url}

    env_vars = [
        ("COMPANY_NAME", name),
        ("COMPANY_EMAIL", email),
        ("COMPANY_PHONE", phone),
        ("COMPANY_ADDRESS", address),
        ("COMPANY_LOGO", logo),
        ("COMPANY_COLOR", color),
        ("COMPANY_IMAGE", image),
    ]

    env_response = set_env_var(account_id, site_id, access_token, env_vars)
    if env_response:
        deploy_response = retry_latest_deploy(site_id, access_token)
        if deploy_response["success"]:
            print(f"Deployed successfully. Deploy ID: {deploy_response['deploy_id']}")
        else:
            print(f"Failed to deploy. Error: {deploy_response['error']}")
    else:
        print(f"Failed to set environment variable. Error: {env_response['error']}")
else:
    print(f"Failed to create site. Error: {site_response}")
