import requests
import json
import tarfile
import yaml
import sys
import logging
import base64
import subprocess

logger = logging.getLogger(__name__)

with open(sys.argv[1]) as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

PRISMA_CLOUD_USERNAME=base64.b64decode(config["prisma-cloud-username"]).decode('utf-8')
PRISMA_CLOUD_PASSWORD=base64.b64decode(config["prisma-cloud-password"]).decode('utf-8')
PRISMA_CLOUD_URL=config["prisma-cloud-url"]

def get_token():

    authenticate_url = PRISMA_CLOUD_URL + "login"

    payload = json.dumps({
        "username": PRISMA_CLOUD_USERNAME,
        "password": PRISMA_CLOUD_PASSWORD
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    response = requests.request("POST", authenticate_url, headers=headers, data=payload)
    token = json.loads(response.text)["token"]
    return token

def get_repo(headers, repo_id):

    repo_url = PRISMA_CLOUD_URL + "bridgecrew/api/v1/cicd/data/runs?repositoryId={}&fetchAllBranches=true&fetchErrors=false".format(repo_id)
    response = requests.request("GET", repo_url, headers=headers)

    return response.text

def main(repo_id):
    FORMAT = '%(asctime)s %(message)s'
    logging.basicConfig(filename='scan_results.log', level=logging.INFO, format=FORMAT)
    token = get_token()
    headers = {
        'Content-Type': 'application/octet-stream',
        'Accept': 'application/json; charset=UTF-8',
        'Authorization': 'Bearer ' + token
    }
    
    print(get_repo(headers, repo_id))

if __name__ == "__main__":
    main(sys.argv[2])