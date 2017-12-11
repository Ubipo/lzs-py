import logging
import argparse
import click
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import sys
import json


'''
=== lzs_server.py ===

Belgium Phone Format OSM Tool by Ubipo:
Converts phone and fax numbers of provided OSM object ids to the ITU-T 'E.164' standard.

Commented lines marked with '$' are for r/w behaviour 
'''

# =======================
# > Variables ===========
# =======================

# Tag names the bot is trying to fix
logFile = 'LzsServer.log' # All messages (DEBUG and up) will be logged
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

  log = logging.getLogger('LzsServer')
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

class Game(object):
  def __init__(self, size):
    log.info('Setting up game...')

    if not (sizeMin <= size <= sizeMax):
      log.error('Fatal error: field size not in range! Exiting...')
      sys.exit()

    self.size = size
    self.playerA = False
    self.playerB = False

    self.fieldA = [['/'] * size] * size
    self.fieldB = [['/'] * size] * size

    log.info(self.fieldA)
    log.info(self.fieldB)


  def handleGET(self, path):
    paths = {'/setup/connect': self.connect,
             '/setup/ready': self.ready,
    }

    return paths[path]()

  def connect(self):
    res = {
      'success': False,
      'playerId': False,
      'size': self.size
    }
    if not(self.playerA and self.playerB):
      if self.playerA:
        self.playerB = 'Ready'
        res['playerId'] = 'B'
      else:
        self.playerA = 'Ready'
        res['playerId'] = 'A'
      res['success'] = True
    else:
      res['playerId']  = False
      res['success'] = False

    return res
  
  def ready(self):
    res = {
      'success': True,
      'ready': (self.playerA and self.playerB),
    }

    return res


class Server():
  def __init__(self, game):
    server_address = ('127.0.0.1', 8081)
    Handler = get_request_handler_with_game(game)
    httpd = HTTPServer(server_address, Handler)

    log.info('Starting server...')
    httpd.serve_forever()


def get_request_handler_with_game(game):

  class ServerRequestHandler(BaseHTTPRequestHandler):

    # GET
    def do_GET(self):
      res = game.handleGET(self.path)

      if res['success']:
        self.send_response(200)
      else:
        self.send_response(500)

      # Send headers
      self.send_header('Content-type','application/json')
      self.end_headers()

      # Write content as utf-8 data
      self.wfile.write(bytes(json.dumps(res), "utf8"))
      return

    def do_POST(self):
      if not ready:
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()

        # Send message back to client
        message = " Connected" + str(self.data_string)
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return

  return ServerRequestHandler


# =======================
# > START ===============
# =======================

# === Click ===
@click.command()

# Options
@click.option('--size', type=int, prompt='> Field size between ' + str(sizeMin) + ' and ' + str(sizeMax), help='Size of the field between ' + str(sizeMin) + ' and ' + str(sizeMax))
@click.option('--verbose', is_flag=True, help='If set, logs debug messages to the console.')
@click.option('--log-level', type=click.Choice(['debug', 'info', 'warning', 'error', 'critical']),  default='info', help='Console logging level, doesn\'t affect file log. Overrides \'--verbose\' flag. Default is info.')


def main(size, verbose, log_level):
  """
  \b
  LAN ZeeSlag:

  """

  # === Setup ===

  # Start the logger
  print('Logging to \'' + logFile + '\'...')
  if verbose:
    startLogger('debug')
  else:
    startLogger(log_level)

  game = Game(size)
  Server(game)

if __name__ == '__main__':
  main()

