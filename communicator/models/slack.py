import communicator.models

class Account:
  pass

class Team:
  pass

class UserProfile:
  first_name              = None
  last_name             = None
  display_name            = None
  display_name_normalized = None
  real_name               = None
  real_name_normalized    = None
  title                   = None
  email                   = None
  phone                   = None
  skype                   = None
  team                  = None
  fields                  = None
  status_text             = None
  status_emoji            = None
  status_expiration       = None
  status_text_canonical   = None
  avatar_hash             = None

  def __init__( self, data ):
  pass

class User:
  id                  = None
  name                = None
  real_name           = None
  team_id             = None
  color               = None
  tz                  = None
  tz_label            = None
  tz_offset           = None
  profile             = None
  updated             = None
  deleted             = False
  is_admin            = False
  is_owner            = False
  is_primary_owner    = False
  is_restricted       = False
  is_ultra_restricted = False
  is_bot              = False
  is_app_user         = False
  has_2fa             = False

  def __init__( self, data ):
    pass


class Bot:
  pass

class Conversation:
  id                         = None
  name                       = None
  name_normalized            = None
  topic                      = {}
  purpose                    = {}
  parent_conversation        = None
  creator                    = None
  created                    = None
  num_members                = None
  previous_names             = []
  shared_team_ids            = []
  pending_shared             = []
  pending_connected_team_ids = []
  unlinked                   = None
  is_channel                 = True
  is_group                   = False
  is_im                      = False
  is_archived                = False
  is_general                 = False
  is_shared                  = False
  is_ext_shared              = False
  is_org_shared              = False
  is_pending_ext_shared      = False
  is_member                  = False
  is_private                 = False
  is_mpim                    = False

  def __init__( self, data ):
    pass

class Message:
  type = None 
  subtype = None
  team = None
  user = None
  text = None
  ts = None
  bot_id = None
  bot_link = None
  bot_profile = None
  pass

class Channel:
  pass

