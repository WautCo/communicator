#!/c/Programs/Python/3.8.5/python

import yaml

from communicator.models import SlackAccount

def main():
  filename = 'Communicator.yml'
  config   = None

  with open( filename ) as file:
    config = yaml.load( file, Loader=yaml.FullLoader )

  accounts = config.get( 'accounts' )
  account  = SlackAccount( accounts[1] )
  client   = account.get_client()
  users    = client.get_team_members()

  print( users[0]['profile']['display_name'] )

if __name__ == '__main__':
  main()
