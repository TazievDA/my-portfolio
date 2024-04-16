import requests


def merge_organizations(api_url, org_ids, preferred_org_id, api_key):
    headers = {'Authorization': f'Bearer {api_key}'}
    data = {
        'orgIds': org_ids,
        'preferredOrgId': preferred_org_id
    }
    response = requests.post(api_url, json=data, headers=headers)
    return response.json()