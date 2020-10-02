#!/c/Programs/Python/3.8.6/python

import argparse

from communicator.app import App

def main():
  parser = argparse.ArgumentParser()

  parser.add_argument( '-V', action='version', version='%(prog)s 0.1.0' )

  args   = parser.parse_args()

  app    = App( )

  app.MainLoop()

if __name__ == '__main__':
  main()
