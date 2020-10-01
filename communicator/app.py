import yaml
import wx

from communicator.components import BuddyList
from communicator.models     import Account

class App( wx.App ):
  buddy_list = None
  services   = {}
  accounts   = {}
  config     = None

  def OnInit( self ):
    filename = 'Communicator.yml'

    with open( filename ) as file:
      self.config   = yaml.load( file, Loader=yaml.FullLoader )

    buddy_list = BuddyList( self.config )

    buddy_list.Show( True )

    self.SetTopWindow( buddy_list )

    for item in self.config.accounts:
      if item['service'] == 'Google':
        account = GoogleAccount( item )
      elif item['service'] == 'Facebook':
        account = FacebookAccount( item )
      elif item['service'] == 'Slack':
        account = SlackAccount( item )
      elif item['service'] == 'WhatsApp':
        account = WhatsAppAccount( item )
      elif item['service'] == 'Skype':
        account = SkypeAccount( item )
      elif item['service'] == 'Twitter':
        account = TwitterAccount( item )

      account.login()

    return True

  def login( self, account ):
    account.login()
    return

  def authorize( self ):
    pass
