#!/usr/bin/env python

import sys

import zmq

from ..pb import price_update_pb2


PORT = 5638
TOPIC = b'price'


def main():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://localhost:{}".format(PORT))

    socket.setsockopt(zmq.SUBSCRIBE, TOPIC)

    while True:
        topic_and_data = socket.recv()
        data = topic_and_data.split(b' ', 1)[1]

        price_update = price_update_pb2.PriceUpdate()
        price_update.ParseFromString(data)

        sys.stdout.write(repr(price_update) + '\n')


if __name__ == '__main__':
    main()
