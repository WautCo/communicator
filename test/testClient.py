#!/c/Programs/Python/3.8.5/python

import yaml

from communicator.models import GoogleAccount, GoogleClient

def main():
  config   = None

  with open( 'Communicator.yml' ) as file:
    config = yaml.load( file, Loader=yaml.FullLoader )

  account  = GoogleAccount( config['accounts'][0] )

  account.login( type='user' )
  account.login( type='service' )

  client   = GoogleClient( account )

  get_spaces( client )

def get_contacts( client ):
  contacts = client.get_contacts()

  for contact in contacts:
    print( contact )

def get_spaces( client ):
  spaces = client.get_spaces()

  for space in spaces:
    print( space )

if __name__ == '__main__':
  main()
