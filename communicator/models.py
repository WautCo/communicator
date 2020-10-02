import os
import pickle
import yaml

from googleapiclient import discovery
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2 import service_account

from communicator.clients import SlackClient

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
  client = None

  def __init__( self, data ):
    self.name     = data['name']
    self.service  = data['service']

    if 'username' in data:
      self.username = data['username']

    if 'password' in data:
      self.password = data['password']

    # self.load_config()

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

  def get_user_credentials( self ):
    return self.user_creds

  def get_service_credentials( self ):
    return self.service_creds

  def set_credentials( self, creds ):
    self.credentials = creds

    return

  def get_config( self ):
    return self.config

  def get_client( self ):
    return self.client

  def set_client( self, client ):
    self.client = client

    return

  def login( self ):
    pass


class GoogleAccount( Account ):
  user_creds    = None
  service_creds = None

  def __init__( self, data ):
    data['service'] = 'Google'

    Account.__init__( self, data )

  def authorize_as_user( self ):
    scopes     = [ 'https://www.googleapis.com/auth/contacts.readonly' ]

    creds      = None
    token_file = os.path.realpath( 'conf/token.pickle' )
    creds_file = os.path.realpath( 'conf/credentials.json' )

    if os.path.exists( token_file ):
        with open( token_file, 'rb' ) as token:
            creds = pickle.load( token )

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh( Request() )
        else:
            flow   = InstalledAppFlow.from_client_secrets_file( creds_file, scopes )
            creds  = flow.run_local_server( port=0 )

        # Save the credentials for the next run
        with open( token_file, 'wb' ) as token:
            pickle.dump( creds, token )

    return creds

  def authorize_as_service( self ):
    scopes       = [ 'https://www.googleapis.com/auth/chat.bot' ]
    key_file     = os.path.realpath( 'conf/key.json' )
    creds        = service_account.Credentials.from_service_account_file( key_file, scopes=scopes )

    return creds

  def login( self, type='user' ):
    creds   = None

    if type == 'user':
      creds = self.authorize_as_user()

      self.user_creds = creds
    elif type == 'service':
      creds = self.authorize_as_service()

      self.service_creds = creds

    return


class FacebookAccount( Account ):
  def login( self ):
    pass


class WhatsAppAccount( Account ):
  def login( self ):
    pass


class SlackAccount( Account ):
  def __init__( self, data ):
    Account.__init__( self, data )

    creds = data.get( 'credentials', {} )
    token = creds.get( 'api_key', '' )

    self.set_client( SlackClient( token ) )


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


class SlackBuddy( Buddy ):
  id                  = None
  name                = None
  real_name           = None
  team_id             = None
  profile             = {}
  tz                  = None
  tz_label            = None
  tz_offset           = None
  updated             = None
  color               = None
  is_admin            = False
  is_owner            = False
  is_primary_owner    = False
  is_restricted       = False
  is_ultra_restricted = False
  is_bot              = False
  is_app_user         = False
  has_2fa             = False
  deleted             = False

  def __init__( self, data ):
    Buddy.__init__( self, data )


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

    user_creds    = account.get_user_credentials()
    service_creds = account.get_user_credentials()
    services      = {
      'people': discovery.build( 'people', 'v1', credentials=user_creds ),
      'chat':   discovery.build( 'chat', 'v1', credentials=service_creds ),
    }

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
    service  = self.services['chat']
    resource = service.spaces()
    request  = resource.list()
    spaces   = request.execute()

    return spaces
