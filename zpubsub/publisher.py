#!/usr/bin/env python


import time
import random

import zmq
import utcdatetime

from pb import price_update_pb2


PORT = 5638


def main():
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:{}".format(PORT))

    time_topic = b'time'
    random_topic = b'random'
    price_topic = b'price'

    while True:
        price_update = price_update_pb2.PriceUpdate()
        price_update.timestamp = str(utcdatetime.utcdatetime.now())
        price_bytes = price_update.SerializeToString()
        socket.send(price_topic + b' ' + price_bytes)

        time_bytes = str(utcdatetime.utcdatetime.now()).encode('utf-8')
        socket.send(time_topic + b' ' + time_bytes)

        random_bytes = str(random.random()).encode('utf-8')
        socket.send(random_topic + b' ' + random_bytes)

        time.sleep(5)


if __name__ == '__main__':
    main()
