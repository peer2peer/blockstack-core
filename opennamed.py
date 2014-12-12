#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Opennamed
    ~~~~~
    :copyright: (c) 2014 by Openname.org
    :license: MIT, see LICENSE for more details.
"""

import argparse
import zerorpc
import daemon
import sys

import config
import logging

log = logging.getLogger()
log.setLevel(logging.DEBUG if config.DEBUG else logging.INFO)
console = logging.StreamHandler()
console.setLevel(logging.DEBUG if config.DEBUG else logging.INFO)
formatter = logging.Formatter('%(message)s')
console.setFormatter(formatter)
log.addHandler(console)

from bitcoinrpc.authproxy import AuthServiceProxy

config_options = 'https://' + config.BITCOIND_USER + ':' + \
    config.BITCOIND_PASSWD + '@' + config.BITCOIND_SERVER + ':' + \
    str(config.BITCOIND_PORT)

bitcoind = AuthServiceProxy(config_options)


class OpennamedRPC(object):
    """ opennamed rpc
    """
    def getinfo(self):
        info = bitcoind.getinfo()
        reply = {}
        reply['blocks'] = info['blocks']
        return reply

    def preorder(self, name, privatekey):
        """ Preorder a name
        """

        log.debug('preorder <%s, %s>' % (name, privatekey))

        return

    def register(self, name, salt, privatekey):
        """ Register a name
        """

        log.debug('register <%s, %s, %s>' % (name, salt, privatekey))

        return

    def update(self, name, data, privatekey):
        """ Update a name
        """

        log.debug('update <%s, %s, %s>' % (name, data, privatekey))

        return

    def transfer(self, name, address, privatekey):
        """ Transfer a name
        """

        log.debug('transfer <%s, %s, %s>' % (name, address, privatekey))

        return

    def renew(self, name, privatekey):
        """ Renew a name
        """

        log.debug('renew <%s, %s>' % (name, privatekey))

        return

    def storedata(self, data):
        """ Store data in DHT
        """

        log.debug('storedata <%s>' % data)

        return

    def getdata(self, hash):
        """ Get data from DHT
        """

        log.debug('getdata <%s>' % hash)

        return


def run_server():
    """ run the opennamed server
    """
    try:
        server = zerorpc.Server(OpennamedRPC())
        server.bind('tcp://' + config.LISTEN_IP + ':' + config.DEFAULT_PORT)
        server.run()
    except Exception as e:
        log.debug(e)
        log.info('Exiting opennamed server')


def stop_server():
    """ Stop the opennamed server
    """
    # Quick hack to kill a background daemon
    import subprocess
    import signal
    import os

    p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    out, err = p.communicate()

    for line in out.splitlines():
        if 'opennamed start' in line:
            log.info('Stopping opennamed server')
            pid = int(line.split(None, 1)[0])
            os.kill(pid, signal.SIGTERM)


def run_opennamed():
    """ run opennamed
    """
    parser = argparse.ArgumentParser(
        description='Openname Core Daemon version {}'.format(config.VERSION))

    parser.add_argument(
        '--bitcoind-server',
        help='the hostname or IP address of the bitcoind RPC server')
    parser.add_argument(
        '--bitcoind-port', type=int,
        help='the bitcoind RPC port to connect to')
    parser.add_argument(
        '--bitcoind-user',
        help='the username for bitcoind RPC server')
    parser.add_argument(
        '--bitcoind-passwd',
        help='the password for bitcoind RPC server')
    subparsers = parser.add_subparsers(
        dest='action', help='the action to be taken')
    parser_server = subparsers.add_parser(
        'start',
        help='start the opennamed server')
    parser_server.add_argument(
        '--foreground', action='store_true',
        help='start the opennamed server in foreground')
    parser_server = subparsers.add_parser(
        'stop',
        help='stop the opennamed server')

    # Print default help message, if no argument is given
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    if args.action == 'start':
        if args.foreground:
            log.info('Starting opennamed server in foreground')
            run_server()
        else:
            log.info('Starting opennamed server')
            with daemon.DaemonContext():
                run_server()
    elif args.action == 'stop':
        stop_server()

if __name__ == '__main__':
    run_opennamed()