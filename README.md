# CICD Scan Results API EndPoints

## Download this repository

## Install dependencies

```pip3 install -r requirements.txt```

## Configuration File (config.yml)

    prisma-cloud-password: #base64encoded secret access key

    prisma-cloud-url: #should be exactly like your prisma cloud console, replace app with api 
    ex. https://api.prismacloud.io/

    prisma-cloud-username: #base64encoded access key id

    code-category:  #Pick one of [Secrets, IacMisconfiguration, Licenses, Vulnerabilities]


## How to run

There are 3 python scripts in this repository:

### get_repositories.py
The purpose of this endpoint: 

    bridgecrew/api/v2/repositories?filter=CICD&page=0&pageSize=100&sortBy=lastScanDate&sortDir=DESC&includeStatus=false

is to obtain the repositories ID that will be used to identify the CICD runIds. It is ordered by the last scanned date of the repositories.

To run:

    python3 get_repositories.py config.yml

### get_runs.py
The purpose of this endpoint: 

    bridgecrew/api/v1/cicd/data/runs?repositoryId=<repo_id>&fetchAllBranches=true&fetchErrors=false

is to obtain the runIds that will be used to obtain scan results from the scan results endpoint. 

To run:

    python3 get_runs.py config.yml <repo_id>

Ex:

    python3 get_runs.py config.yml 43de2057-e942-4834-b52f-d7327b1f9137

### get_resources.py
The purpose of this endpoint: 

    bridgecrew/api/v2/errors/code_review_scan/resources

is to obtain the resources that will be used to obtain scan results from the scan results endpoint. 

To run:

    python3 get_resources.py config.yml <repo_id> <runId>

Ex:

    python3 get_resources.py config.yml bbaa2b2d-d6ea-41f7-ae15-b4c73709a8e8 1023293

### cicd_scan_results.py
The purpose of this endpoint: 

    bridgecrew/api/v2/errors/code_review_scan/resources/policies

is to obtain the scan results from the provided repository, resource, and runId. 

To run:

    python3 get_runs.py config.yml <repo_id> <resource_name> <runId>

Ex:

    python3 cicd_scan_results.py config.yml 43de2057-e942-4834-b52f-d7327b1f9137 /planfile.json:azurerm_storage_account.storage_account 1159120      

