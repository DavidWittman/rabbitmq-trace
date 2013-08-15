#!/usr/bin/env python
'''
rabbitmq trace scripts.

require (rabbitmq_tracing):
    $ sudo rabbitmq-plugins enable rabbitmq_tracing

usage:
    $ sudo rabbitmqctl trace_on
    $ ./rabbitmqtrace.py
    << output >>
'''
import sys
import time

from optparse import OptionParser

from kombu import Connection, Exchange, Queue
from kombu.mixins import ConsumerMixin
from kombu.utils import debug, log

logger = log.get_logger(__name__)

class FirehoseDrinker(ConsumerMixin):
    def __init__(self, connection):
        self.connection = connection

    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=_get_queues(), callbacks=[self.process_task])]

    def process_task(self, body, message):
        print("Got message: {}".format(reprcall(body)))
        message.ack()

def _get_queues():
    exchange = Exchange('amq.rabbitmq.trace', type='topic')
    return [Queue('firehose', exchange, routing_key='#')]

def _run(options):
    host = options.host
    user = options.user
    password = options.password
    vhost = options.vhost
    port = options.port

    with Connection(host, user, password, vhost, port) as conn:
        try:
            FirehoseDrinker(conn).run()
        except KeyboardInterrupt:
            print('Exiting')

def main():
    debug.setup_logging(loglevel=10)
    parser = OptionParser('usage: %prog')
    parser.add_option('', '--host', metavar='host', default='localhost', help='rabbitmq host address, default: %default')
    parser.add_option('', '--port', metavar='port', default=5672, type='int', help='rabbitmq port, default: %default')
    parser.add_option('', '--vhost', metavar='vhost', default='/', help='rabbitmq vhost, default: %default')
    parser.add_option('', '--user', metavar='user', default='guest', help='rabbitmq user, default: %default')
    parser.add_option('', '--password', metavar='password', default='guest', help='rabbitmq password, default: %default')

    (options, args) = parser.parse_args()
    _run(options)

if __name__ == '__main__':
    main()
