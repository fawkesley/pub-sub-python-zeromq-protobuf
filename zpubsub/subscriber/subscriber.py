#!/usr/bin/env python

import logging
import sys
import os

import zmq

from ..pb import price_update_pb2
from ..utils import load_key_pair


PUBLISHER_IP = '10.0.2.15'
PORT = 5638
TOPIC = b'price'
KEYS_DIR = os.path.join(os.path.dirname(__file__), 'keys')


def main():
    logging.basicConfig(level=logging.DEBUG)

    socket = make_socket()

    while True:
        topic_and_data = socket.recv()
        data = topic_and_data.split(b' ', 1)[1]

        price_update = price_update_pb2.PriceUpdate()
        price_update.ParseFromString(data)

        sys.stdout.write(repr(price_update) + '\n')


def make_socket():
    context = zmq.Context()

    socket = context.socket(zmq.SUB)

    configure_socket_keys(socket)
    connect_and_subscribe_socket(socket)

    return socket


def connect_and_subscribe_socket(socket):
    socket.connect("tcp://{ip}:{port}".format(ip=PUBLISHER_IP, port=PORT))
    socket.setsockopt(zmq.SUBSCRIBE, TOPIC)


def configure_socket_keys(s):
    s.curve_publickey, s.curve_secretkey = load_key_pair(
        KEYS_DIR, 'subscriber', generate_on_fail=True
    )

    s.curve_serverkey = load_publisher_public_key('publisher')


def load_publisher_public_key(name):
    publisher_public_file = os.path.join(KEYS_DIR, 'publisher.public.key')
    if not os.path.isfile(publisher_public_file):
        raise RuntimeError(
            "Missing public key for publisher: I'm unable to connect and "
            "authenticate the publisher. Copy {} to {} ".format(
                os.path.basename(publisher_public_file),
                os.path.abspath(KEYS_DIR))
        )

    publisher_public, _ = zmq.auth.load_certificate(publisher_public_file)
    return publisher_public


if __name__ == '__main__':
    main()
