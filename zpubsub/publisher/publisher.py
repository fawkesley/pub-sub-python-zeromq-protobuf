#!/usr/bin/env python


import time
import random

import zmq
import utcdatetime

from ..pb import price_update_pb2


PORT = 5638
TIME_TOPIC = b'time'
RANDOM_TOPIC = b'random'
PRICE_TOPIC = b'price'


def main():
    socket = make_socket()

    while True:
        send_messages(socket)
        time.sleep(5)


def make_socket():
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:{}".format(PORT))
    return socket


def send_messages(socket):
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
