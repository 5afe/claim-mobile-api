# claim-mobile-api
Mobile client gateway for claim token flow


## Setup

Following steps will guide through initial creation of guardians and vestings database which is needed for the service to operate.

### Infura

[Infura](https://infura.io/) is used as web3 provider to communicate with the blockchain. You need to get an API key and create environmental variable `INFURA_PROJECT_ID`
```
export INFURA_PROJECT_ID=<YOUR_PROJECT_ID>
```

### Populate data

Run bootstrap script to parse guardians from csv, resolve their addresses, and download their images. Images will be converted to JPG, resized keeping initial aspect ratio, and stored in three different sizes.
```
python bootstrap.py
```

### Run service
Start service by running
```
uvicorn app:app --reload
```

### Endpoints
By default swagger UI is accessible at
```
http://127.0.0.1:8000/docs
```
Redoc UI is accessible at
```
http://127.0.0.1:8000/redoc
```
