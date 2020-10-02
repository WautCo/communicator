#!/c/Programs/Python/3.8.5/python

from googleapiclient import discovery
from google.oauth2 import service_account

def main():
  file     = 'key.json'
  scopes   = [
    'https://www.googleapis.com/auth/chat.bot',
  ]

  creds    = service_account.Credentials.from_service_account_file( file, scopes=scopes )
  api      = discovery.build( 'chat', 'v1', credentials=creds )
  request  = api.spaces().list( pageSize=100 )
  response = request.execute()

  for item in response:
    print( item )

if __name__ == '__main__':
  main()
else:
  print( __name__ )
