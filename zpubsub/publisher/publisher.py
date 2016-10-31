#!/usr/bin/env python


import logging
import os
import random
import time

import zmq
import zmq.auth
from zmq.auth.thread import ThreadAuthenticator

import utcdatetime

from ..pb import price_update_pb2
from ..utils import load_key_pair


PORT = 5638
TIME_TOPIC = b'time'
RANDOM_TOPIC = b'random'
PRICE_TOPIC = b'price'
KEYS_DIR = os.path.join(os.path.dirname(__file__), 'keys')


def main():
    logging.basicConfig(level=logging.DEBUG)

    socket, authenticator = make_socket_and_authenticator()

    assert authenticator.is_alive()

    try:
        while True:
            send_messages(socket)
            time.sleep(5)

    except KeyboardInterrupt:
        authenticator.stop()
        raise


def make_socket_and_authenticator():
    context = zmq.Context()

    authenticator = make_authenticator(context)

    socket = context.socket(zmq.PUB)

    configure_socket_keys(socket)

    socket.bind("tcp://*:{}".format(PORT))

    return socket, authenticator


def make_authenticator(context):
    auth = ThreadAuthenticator(context)
    auth.start()
    # Note: by omitting auth.allow(ip) we're allowing connection from any IP

    auth.configure_curve(
        domain='*',
        # CURVE_ALLOW_ANY: allow all client keys without checking
        location=zmq.auth.CURVE_ALLOW_ANY
    )
    return auth


def configure_socket_keys(s):
    (s.curve_publickey, s.curve_secretkey) = load_key_pair(
        KEYS_DIR, 'publisher', generate_on_fail=True
    )
    s.curve_server = True


def send_messages(socket):
    logging.debug("Sending messages to topics.")
    price_bytes = make_price_update_bytes()
    socket.send(PRICE_TOPIC + b' ' + price_bytes)

    time_bytes = str(utcdatetime.utcdatetime.now()).encode('utf-8')
    socket.send(TIME_TOPIC + b' ' + time_bytes)

    random_bytes = str(random.random()).encode('utf-8')
    socket.send(RANDOM_TOPIC + b' ' + random_bytes)


def make_price_update_bytes():
    price_update = price_update_pb2.PriceUpdate()
    price_update.timestamp = str(utcdatetime.utcdatetime.now())
    price_bytes = price_update.SerializeToString()
    return price_bytes


if __name__ == '__main__':
    main()
