import logging
import argparse
import click
import time
import requests
import sys
import json
import time


'''
=== lzs_client.py ===

Belgium Phone Format OSM Tool by Ubipo:
Converts phone and fax numbers of provided OSM object ids to the ITU-T 'E.164' standard.

Commented lines marked with '$' are for r/w behaviour 
'''

# =======================
# > Variables ===========
# =======================

# Tag names the bot is trying to fix
logFile = 'BpfOsmTool.log' # All messages (DEBUG and up) will be logged
sizeMin = 2
sizeMax = 20


# =======================
# > Declarations ========
# =======================

log = None

# Logger
def startLogger(clLevel):
  global log

  clLevelNum = getattr(logging, clLevel.upper(), None)

  formatCl = logging.Formatter(fmt='{levelname: <9} {message}', style='{')
  formatFile = logging.Formatter(fmt='{asctime: <24} {levelname: <9} {message}', style='{')

  log = logging.getLogger('BpfOsmTool')
  log.setLevel(logging.DEBUG)

  # Create command line and file handlers
  ch = logging.StreamHandler()
  ch.setLevel(clLevelNum)
  ch.setFormatter(formatCl)

  fh = logging.FileHandler(logFile, mode='a')
  fh.setLevel(logging.DEBUG)
  fh.setFormatter(formatFile)

  log.addHandler(ch)
  log.addHandler(fh)

def drawField(field, title):
  colsNbr = len(field);
  rowsNbr = len(field[0]);

  # Title
  print(' '*round((5*colsNbr-(len(title)))/2), end="", flush=True) # Start
  print(title, end="", flush=True) # Title
  print('', flush=True) # Stop

  # Top box drawing
  print('┌───┬', end="", flush=True) # Start
  for i in range(rowsNbr-1): # Middle
    print('───', end="┬", flush=True)
  print('───┐', flush=True) # Stop

  # Column header
  print('│   │ ', end="", flush=True) # Start
  for i in range(rowsNbr): # Middle
    print(chr(65 + i), end=" │ ", flush=True)
  print('', flush=True) # Stop

  # Rows
  for i, row in enumerate(field):
    # Horizontal seperator
    print('├───┼', end="", flush=True) # Start
    for j in range(rowsNbr-1): # Middle
      print('───┼', end="", flush=True)
    print('───┤', flush=True) # Stop

    # Row heading
    print('│ ' + str(i), end=" │ ", flush=True)

    # Row
    for cel in field[i]:
      print(cel, end=" │ ", flush=True)
    print('', flush=True) # Stop
  
  # Bottom box drawing
  print('└───┴', end="", flush=True) # Start
  for i in range(rowsNbr-1): # Middle
    print('───', end="┴", flush=True)
  print('───┘', flush=True) # Stop



# =======================
# > START ===============
# =======================

# === Click ===
@click.command()

# Options
@click.option('--ip', prompt='> IP and port of the server', help='IP and port of the server.')
@click.option('--verbose', is_flag=True, help='If set, logs debug messages to the console.')
@click.option('--log-level', type=click.Choice(['debug', 'info', 'warning', 'error', 'critical']),  default='info', help='Console logging level, doesn\'t affect file log. Overrides \'--verbose\' flag. Default is info.')


def main(ip, verbose, log_level):
  """
  \b
  LAN ZeeSlag client:

  """

  # === Setup ===

  # Start the logger
  print('Logging to \'' + logFile + '\'...')
  if verbose:
    startLogger('debug')
  else:
    startLogger(log_level)


  # Check if URL is provided
  log.info('Setting up game...')

  log.info('Connecting to server...')

  res = requests.get(url='http://' + ip + '/setup/connect', allow_redirects=True).json()

  if not res['success']:
    log.error('Error connecting, a game might already be in progress')
    sys.exit()

  playerId = res['playerId']
  size = res['size']

  log.info('Succesfully connected! You\'re player '+playerId+', board size is '+str(size))

  gameReady = False
  log.info('Waiting for other player to ready up...')

  while True:
    res = requests.get(url='http://' + ip + '/setup/ready', allow_redirects=True).json()
    if (res['ready']):
      break
    else:
      time.sleep(0.5)
      print('.', end="", flush=True)
  
  log.info('Game starting...')

  print('')

  fieldY = [[' '] * size] * size # Your field
  fieldO = [[' '] * size] * size # Opponent`s field
  drawField(fieldY, 'My field')

  for i in boats:
    print('Please input location of boat '+boatI)

  # === Exit ===
  log.info('Done! Exiting...')

if __name__ == '__main__':
    main()

