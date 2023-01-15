import requests
def refresh_access_token(refresh_token):
    # Set the API endpoint and request parameters
    endpoint = 'https://oauth2.googleapis.com/token'
    data = {
    'client_secret': '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',
    'grant_type': 'refresh_token',
    'refresh_token': refresh_token,
    'client_id': '164520596220-leevtqd6pgh5vhnv799s17chkm5ukd3d.apps.googleusercontent.com'
    }

    # Send the POST request
    response = requests.post(endpoint, data=data)

    # Extract the access token from the response
    access_token = response.json()['access_token']

    return access_token

print(refresh_access_token('1//04Ff8B7MhZWiWCgYIARAAGAQSNwF-L9IruojbZefFbDSsbnQrCb6a1XLsm9SNqrlagS7hw7ATcmUKQt-Gufc2mZDXS9apgAfRDMU'))