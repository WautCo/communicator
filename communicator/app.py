import logging
import os
import wx
import yaml

from communicator.components import BuddyList
from communicator.models     import GoogleAccount, SlackAccount

class App( wx.App ):
  config   = None
  accounts = {}

  def OnInit( self ):
    filename = os.path.realpath( 'conf/Communicator.yml' )
    config   = None
    loger    = None

    with open( filename ) as file:
      config = yaml.load( file, Loader=yaml.FullLoader )

    accounts = config.get( 'accounts', None )

    if accounts is None:
      wx.MessageBox( 'Please add accounts to the config' )

      return

    self.config = config

    self.configure_logging()

    for item in accounts:
      service = item.get( 'service', None )

      if service == 'Google':
        account = GoogleAccount( item )
      elif service == 'Facebook':
        account = FacebookAccount( item )
      elif service == 'Slack':
        account = SlackAccount( item )
      elif service == 'WhatsApp':
        account = WhatsAppAccount( item )
      elif service == 'Skype':
        account = SkypeAccount( item )
      elif service == 'Twitter':
        account = TwitterAccount( item )

      account.login()

      self.accounts[account.get_name()] = account

    buddy_list = BuddyList( self )

    buddy_list.Show( True )

    self.SetTopWindow( buddy_list )

    return True

  def configure_logging( self ):
    logger = logging.getLogger()

    logger.setLevel( logging.DEBUG )

    self.logger = logger

    return

  def get_accounts( self ):
    return self.accounts

  def get_config( self ):
    return self.config

  def get_logger( self ):
    return self.logger
