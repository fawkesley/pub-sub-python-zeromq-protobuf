#!/usr/bin/env python

import sys

import zmq


PORT = 5638
TOPIC = b'time'


def main():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://localhost:{}".format(PORT))

    socket.setsockopt(zmq.SUBSCRIBE, TOPIC)

    while True:
        topic_and_data = socket.recv()
        data = topic_and_data.split(b' ', 1)[1]

        sys.stdout.write(repr(data) + '\n')


if __name__ == '__main__':
    main()
