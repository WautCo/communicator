import os
import logging

from flask import Flask
from slack import WebClient

class Client:
  def __init__( self ):
    pass

  def connect( self ):
    pass


class SlackClient( Client ):
  web_client    = None

  def __init__( self, token ):
    Client.__init__( self )

    client = WebClient( token=token )

    self.web_client = client

  def get_team_name( self ):
    name     = None
    response = self.web_client.team_info()

    if response['ok']:
      team   = response.get( 'team' )
      name   = team.get( 'name' )

    return name

  def get_team_members( self ):
    users    = None
    response = self.web_client.users_list()

    if response['ok']:
      users  = response.get( 'members' )

    return users


class FacebookClient( Client ):
  def __init__( self ):
    Client.__init__( self )


class GoogleClient( Client ):
  def __init__( self ):
    Client.__init__( self )


class WhatsAppClient( Client ):
  def __init__( self ):
    Client.__init__( self )


class TwitterClient( Client ):
  def __init__( self ):
    Client.__init__( self )


class SkypeClient( Client ):
  def __init__( self ):
    Client.__init__( self )
