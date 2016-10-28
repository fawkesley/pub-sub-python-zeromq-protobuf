#!/usr/bin/env python


import time
import random

import zmq
import utcdatetime


PORT = 5638


def main():
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:{}".format(PORT))

    time_topic = b'time'
    random_topic = b'random'

    while True:
        time_bytes = str(utcdatetime.utcdatetime.now()).encode('utf-8')
        socket.send(time_topic + b' ' + time_bytes)

        random_bytes = str(random.random()).encode('utf-8')
        socket.send(random_topic + b' ' + random_bytes)

        time.sleep(5)


if __name__ == '__main__':
    main()
