#!/usr/bin/python
# -----------------------------------------------------------
# Python3 script that uploads an IP Address to Maltiverse (Requires Enterprise Plan)
#
# (C) 2023 maltiverse.com
# Released under CC0 1.0 Universal
# -----------------------------------------------------------

import requests
import json

# REPLACE WITH YOUR LOGIN CREDENTIALS
MALTIVERSE_EMAIL = ""
MALTIVERSE_PASSWORD = ""

# SPECIFY YOUR TEAM NAME (Look for it at Maltiverse.com)
MALTIVERSE_TEAM = ""


def upload_ip_to_maltiverse():
    api_url = "https://api.maltiverse.com"
    endpoint = "/ip/"

    # Authentication in Maltiverse
    HEADERS = {}
    login_obj = {
        "email": MALTIVERSE_EMAIL,
        "password": MALTIVERSE_PASSWORD,
    }
    try:
        data_login = requests.post(
            "https://api.maltiverse.com/auth/login", json=login_obj
        )
        R_JSON = json.loads(data_login.text)
        if "status" in R_JSON and R_JSON["status"] == "success":
            if R_JSON["auth_token"]:
                HEADERS = {"Authorization": "Bearer " + R_JSON["auth_token"]}
            else:
                print("Authentication failed")
                raise SystemExit()
        else:
            print("Authentication failed")
            raise SystemExit()

    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    # Define IP Object document to upload following the specification:
    # https://app.swaggerhub.com/apis-docs/maltiverse/api/1.1.2#/IpItem
    ip_doc = {
        "type": "ip",
        "ip_addr": "89.238.73.97",
        "classification": "malicious",
        "blacklist": [
            {
                "description": "Eicar",
                "source": MALTIVERSE_TEAM,
            }
        ],
    }

    # Upload
    try:
        response = requests.put(
            api_url + endpoint + ip_doc["ip_addr"], headers=HEADERS, json=ip_doc
        )
        response.raise_for_status()  # Raise an error for bad responses
        result = response.json()
        print("Upload successful. Result:", result)
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Something went wrong: {err}")


if __name__ == "__main__":
    upload_ip_to_maltiverse()
