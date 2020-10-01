import wx

from communicator.models import Service, Account, Buddy, Group

class Conversation( wx.Frame ):
  MSG_BOX_ID = 1001
  SEND_ID = 1002
  recipients = []

  def __init__( self, parent, title ):
    id       = -1
    position = wx.DefaultPosition
    size = wx.Size( 450, 450 )
    style = wx.DEFAULT_FRAME_STYLE | wx.MAXIMIZE

    wx.Frame.__init__( self, parent, id, title, position, size, style )

    self.configure_menus()
    self.configure_components()

  def configure_menus( self ):
    menu_bar   = wx.MenuBar()
    convo_menu = wx.Menu()
    edit_menu = wx.Menu()
    view_menu = wx.Menu()
    tools_menu = wx.Menu()
    help_menu  = wx.Menu()

    invite_item = convo_menu.Append( -1, "Add People...\TCtrl-I", "Invite buddies to join this conversation" )

    convo_menu.AppendSeparator()

    exit_item = convo_menu.Append( wx.ID_EXIT, "Exit\tCtrl-Q" )
    about_item = help_menu.Append( wx.ID_ABOUT )

    menu_bar.Append( convo_menu, "Conversation" )
    menu_bar.Append( edit_menu, "Edit" )
    menu_bar.Append( view_menu, "View" )
    menu_bar.Append( tools_menu, "Tools" )
    menu_bar.Append( help_menu, "Help" )

    self.SetMenuBar( menu_bar )

    self.Bind( wx.EVT_MENU, self.on_invite, invite_item )
    self.Bind( wx.EVT_MENU, self.on_about, about_item )
    self.Bind( wx.EVT_MENU, self.on_exit, exit_item )

    return

  def configure_components( self ):
    main_panel = wx.Panel( self )
    hist_panel = wx.ScrolledWindow( main_panel )
    msg_panel = wx.Panel( main_panel )
    main_sizer = wx.BoxSizer( wx.VERTICAL )
    hist_sizer = wx.BoxSizer( wx.VERTICAL )
    msg_sizer = wx.BoxSizer( wx.HORIZONTAL )
    convo_view = wx.TextCtrl( hist_panel, -1, "", wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY|wx.TE_MULTILINE )
    msg_box = wx.TextCtrl( msg_panel, self.MSG_BOX_ID, "", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER|wx.TE_MULTILINE|wx.TE_WORDWRAP  )
    send_button = wx.Button( msg_panel, self.SEND_ID, "Send" )

    main_panel.SetSizer( main_sizer )
    msg_panel.SetSizer( msg_sizer )
    hist_panel.SetSizer( hist_sizer )

    hist_sizer.Add( convo_view )

    msg_sizer.Add( msg_box )
    msg_sizer.Add( send_button )

    main_sizer.Add( hist_panel  )
    main_sizer.Add( msg_panel )

    self.CreateStatusBar()
    self.SetStatusText( "" )

    msg_box.Bind( wx.EVT_TEXT_ENTER, self.on_enter, msg_box )
    send_button.Bind( wx.EVT_BUTTON, self.on_enter, send_button )

    return

  def add_recipient( self, buddy ):
    self.recipients.append( buddy )
    return

  def on_enter( self, event ):
    wx.MessageBox( "Message Sent" )

    return

  def on_invite( self, event ):
    item = event.GetItem()

    return

  def on_about( self, event ):
    message = "This is the Communicator application"
    title = "Communicator"
    flags = wx.OK | wx.ICON_INFORMATION

    wx.MessageBox()

    return

  def on_exit( self, event ):
    self.Close( True )

    return

class BuddyList( wx.Frame ):
  TREE_ID   = 1000
  tree_ctrl = None
  config    = None
  groups    = {}
  buddies   = {}
  accounts = {}

  def __init__( self, config=None ):
    id       = -1
    title    = "Communicator - Buddy List"
    position = wx.DefaultPosition
    size     = wx.Size( 450, 450 )
    style = wx.DEFAULT_FRAME_STYLE|wx.MAXIMIZE

    self.config = config

    wx.Frame.__init__( self, None, id, title, position, size, style )

    self.configure_menus()
    self.configure_components()

  def configure_menus( self ):
    menu_bar = wx.MenuBar()
    app_menu = wx.Menu()
    convos_menu = wx.Menu()
    buddies_menu = wx.Menu()
    help_menu = wx.Menu()

    exit_item = app_menu.Append( wx.ID_EXIT, "Exit\tCtrl-Q" )

    new_convo_item = convos_menu.Append( -1, "New Conversation...\tCtrl-N", "Starts a new conversation" )
    add_buddy_item = buddies_menu.Append( -1, "Add Buddy...", "Add a new buddy" )
    about_item = help_menu.Append( wx.ID_ABOUT )

    menu_bar.Append( convos_menu, "Conversations" )
    menu_bar.Append( buddies_menu, "Buddies" )
    menu_bar.Append( app_menu, "Application" )
    menu_bar.Append( help_menu, "Help" )

    self.SetMenuBar( menu_bar )

    self.Bind( wx.EVT_MENU, self.on_new_convo, new_convo_item )
    self.Bind( wx.EVT_MENU, self.on_add_buddy, add_buddy_item )
    self.Bind( wx.EVT_MENU, self.on_about, about_item )
    self.Bind( wx.EVT_MENU, self.on_exit, exit_item )

    return

  def configure_components( self ):
    panel     = wx.Panel( self )
    sizer     = wx.BoxSizer( wx.VERTICAL )
    label     = wx.StaticText( panel, label="Buddy List" )
    tree      = wx.TreeCtrl( panel, self.TREE_ID )

    self.tree_ctrl = tree

    self.populate_tree()

    sizer.Add( label, wx.SizerFlags().Border( wx.TOP|wx.LEFT, 25 ) )
    sizer.Add( tree, wx.SizerFlags().Border( wx.BOTTOM|wx.LEFT, 25 ) )

    panel.SetSizer( sizer )

    self.CreateStatusBar()
    self.SetStatusText( "Ready" )

    return

  def create_conversation( self, buddy ):
    name  = buddy.get_name()
    title = f"{name}"
    convo = Conversation( self, title )

    convo.add_recipient( buddy )

    return convo

  def populate_tree( self ):
    accounts = self.config['accounts']
    groups  = self.config['groups']
    buddies = self.config['buddies']
    tree    = self.tree_ctrl
    nodes   = {}

    tree.SetWindowStyle( wx.TR_SINGLE | wx.TR_LINES_AT_ROOT | wx.TR_EDIT_LABELS | wx.TR_HIDE_ROOT )

    root      = tree.AddRoot( "Groups" )

    for item in accounts:
      account = Account( item )
      name    = account.get_name()

      self.accounts[name] = account

    for item in groups:
      group = Group( item )
      name   = group.get_name()

      nodes[name] = tree.AppendItem( root, name, -1, -1, group )

      self.groups[name] = group

    for item in buddies:
      buddy = Buddy( item )
      name  = buddy.get_name()
      group = buddy.get_group()
      node  = nodes[group]

      tree.AppendItem( node, buddy.get_name(), -1, -1, buddy )

      self.buddies[name] = buddy

    child = tree.GetFirstChild( root )

    tree.EnsureVisible( child[0] )

    tree.Bind( wx.EVT_TREE_ITEM_ACTIVATED, self.on_item_activated,      id=self.TREE_ID )
    tree.Bind( wx.EVT_TREE_ITEM_MENU, self.on_tree_context_menu, id=self.TREE_ID )
    tree.Bind( wx.EVT_TREE_SEL_CHANGED, self.on_tree_selection,         id=self.TREE_ID )

    return

  def on_new_convo( self, event ):
    item   = self.tree_ctrl.GetSelection()
    object = self.tree_ctrl.GetItemData()

    wx.MessageBox( object.__name__ )

    if object.__name__ == "Group":
      return

    convo  = self.create_conversation( object )

    convo.Show( True )

    return

  def on_add_buddy( self, event ):
    wx.MessageBox( "New Buddy!" )

    return

  def on_item_activated( self, event ):
    item   = event.GetItem()
    object = self.tree_ctrl.GetItemData( item )
    obj_class  = object.__class__

    if obj_class is Group:
      wx.MessageBox( f'{obj_class}' )
      return

    convo = self.create_conversation( object )

    convo.Show( True )

    return

  def on_tree_context_menu( self, event ):
    item   = event.getItem()
    object = self.tree_ctrl.GetItemData( item )

    return

  def on_tree_selection( self, event ):
    item   = event.GetItem()
    object = self.tree_ctrl.GetItemData( item )

    return

  def on_about( self, event ):
    message = "This is the Communicator application"
    title = "Communicator"
    flags = wx.OK | wx.ICON_INFORMATION

    wx.MessageBox( message, title, flags )

    return

  def on_exit( self, event ):
    self.Close( True )

    return
