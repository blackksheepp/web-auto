import requests as r
import json

company_name = "razorsay"
email = "razorsays@me.com"
phone = "+212-313-4114"

url = "https://api.netlify.com/api/v1/sites"

headers = {
    "Authorization": "Bearer nfp_GJCt9NynJD3d2U1WBxRND4eHqYzJ16wce6d3",
    "Content-Type": "application/json",
}

payload = {
    "name": company_name,
    "repo": {
        "provider": "github",
        "repo_path": "blackksheepp/web-auto-template",
        "repo_branch": "main",
        "cmd": "npm install && npm run start",
        "dir": "dist",
        "private": False,
        "env": {
            "COMPANY_NAME": company_name,
            "COMPANY_EMAIL": email,
            "COMPANY_PHONE": phone,
        },
        "allowed_branches": ["main"],
        "base": ".",
        "installation_id": 56525149,
    },
}

response = r.post(url, headers=headers, data=json.dumps(payload))
