#!/c/Programs/Python/3.8.5/python

from daemoniker import Daemonizer

def main():
  pid_file = 'Communicator.pid'
  number   = 1

  with Daemonizer() as ( is_setup, daemonizer ):
    if is_setup:
      pass

    is_parent, *args = daemonizer( pid_file, 1000 )

    if is_parent:
      pass

  with open( 'test.txt', 'w' ) as file:
    while number <= args[0]:
      print( number )
      file.write( f'{number}\n' )

      number += 1

if __name__ == '__main__':
  main()
