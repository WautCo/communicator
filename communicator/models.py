import pickle
import yaml

import os.path

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class Service:
  name   = None
  server = None

  def __init__( self, data ):
    self.name = data['name']

  def get_name( self ):
    return self.name

  def __str__( self ):
    return self.name


class Account:
  name          = None
  service       = None
  configuration = None
  credentials   = None
  username      = None
  password      = None

  def __init__( self, data ):
    self.name     = data['name']
    self.service  = data['service']

    if 'username' in data:
      self.username = data['username']

    if 'password' in data:
      self.password = data['password']

    self.load_config()

  def load_config( self ):
    config = None

    with open( 'Communicator.yml' ) as file:
      config = yaml.load( file, Loader=yaml.FullLoader )

    self.configuration = config

    return

  def get_name( self ):
    return self.name

  def get_service( self ):
    return self.service

  def get_username( self ):
    return self.username

  def get_password( self ):
    return self.password

  def get_credentials( self ):
    return self.credentials

  def set_credentials( self, creds ):
    self.credentials = creds

    return

  def get_config( self ):
    return self.config

  def login( self ):
    pass


class GoogleAccount( Account ):
  SCOPES      = {
    'people': [
      'https://www.googleapis.com/auth/contacts.readonly',
    ],
    'chat':   [
      'https://www.googleapis.com/auth/chat',
      # 'https://www.googleapis.com/auth/chat.bot'
    ],
  }

  credentials = None

  def __init__( self, data ):
    data['service'] = 'Google'

    Account.__init__( self, data )

  def authorize( self ):
    creds      = None
    token_file = 'token.pickle'
    creds_file = 'credentials.json'

    if os.path.exists( token_file ):
        with open( token_file, 'rb' ) as token:
            creds = pickle.load( token )

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh( Request() )
        else:
            scopes = self.SCOPES['chat']
            flow   = InstalledAppFlow.from_client_secrets_file( creds_file, scopes )
            creds  = flow.run_local_server( port=0 )

        # Save the credentials for the next run
        with open( token_file, 'wb' ) as token:
            pickle.dump( creds, token )

    return creds

  def login( self ):
    creds = self.authorize()

    self.credentials = creds

    return


class FacebookAccount( Account ):
  def login( self ):
    pass


class WhatsAppAccount( Account ):
  def login( self ):
    pass


class SlackAccount( Account ):
  def login( self ):
    pass


class SkypeAccount( Account ):
  def login( self ):
    pass


class TwitterAccount( Account ):
  def login( self ):
    pass


class Buddy:
  name    = None
  alias   = None
  account = None
  group   = None

  def __init__( self, data ):
    self.name = data['name']
    self.account = data['account']
    self.alias = data['alias']
    self.group = data['group']

  def get_name( self ):
    return self.name

  def get_group( self ):
    return self.group

  def set_group( self, group ):
    self.group = group

    return

  def __str__( self ):
    return self.name


class Group:
  name    = None
  buddies = None

  def __init__( self, data ):
    self.name = data['name']

  def get_name( self ):
    return self.name

  def get_buddies( self ):
    return self.buddies

  def add_buddy( self, buddies ):
    self.buddies[buddy.get_name()] = buddy

    return

  def remove_buddy( self, buddy ):
    return

  def __str__( self ):
    return self.name


class Client:
  account = None

  def __init__( self, account ):
    self.account = account

  def get_contact_groups( self ):
    groups = []

    return groups

  def get_contacts():
    contacts = []

    return contacts


class GoogleClient( Client ):
  services = None

  def __init__( self, account ):
    Client.__init__( self, account )

    creds    = account.get_credentials()
    services = {}

    services['people'] = build( 'people', 'v1', credentials=creds )
    services['chat'] = build( 'chat', 'v1', credentials=creds )

    self.services = services

  def get_contacts( self ):
    max         = 1000
    resource    = 'people/me'
    fields      = 'names,emailAddresses'
    # options     = ( resourceName=resource, pageSize=max, personFields=fields )
    collection  = self.services['people'].people()
    results     = collection.connections().list( resourceName=resource, pageSize=max, personFields=fields ).execute()
    connections = results.get( 'connections', [] )

    return connections

  def get_spaces( self ):
    spaces = self.services['chat'].spaces().list().execute()

    return spaces
