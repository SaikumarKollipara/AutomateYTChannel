endpoint = 'https://oauth2.googleapis.com/token'
data = {
'client_secret': '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',
'grant_type': 'refresh_token',
'refresh_token': '1//04OPW9e4h1CMuCgYIARAAGAQSNwF-L9IrgjICJoAcm4qx4ROhxlHuDvKo2PdeKKS5f68SIAdFSLfpce_wkTGKfWHnJq5ZoFdHldc',
'client_id': '164520596220-leevtqd6pgh5vhnv799s17chkm5ukd3d.apps.googleusercontent.com'
}

# Send the POST requestṇ
response = requests.post(endpoint, data=data)

# Extract the access token from the response
access_token = response.json()['access_token']