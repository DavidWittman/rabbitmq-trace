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
import pika

__AUTHOR__  = 'smallfish'
__VERSION__ = '0.0.1'

def _out(args):
    print time.strftime('%Y-%m-%d %H:%M:%S'), args

def _run(host, port, vhost, user, password):
    conn = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port, virtual_host=vhost,
        credentials=pika.PlainCredentials(user, password)))
    chan = conn.channel()
    def _on_message(ch, method, properties, body):
        ret = {}
        ret['routing_key'] = method.routing_key
        ret['headers'] = properties.headers
        ret['body'] = body
        _out(ret)
    _out('start subscribe amq.rabbitmq.trace')
    ret = chan.queue_declare(exclusive=False, auto_delete=True)
    queue = ret.method.queue
    chan.queue_bind(exchange='amq.rabbitmq.trace', queue=queue, routing_key='#')
    chan.queue_bind(exchange='amq.rabbitmq.log', queue=queue, routing_key='#')
    chan.basic_consume(_on_message, queue=queue, no_ack=True)
    chan.start_consuming()

def main():
    parser = OptionParser('usage: %prog')
    parser.add_option('', '--host', metavar='host', default='localhost', help='rabbitmq host address, default: %default')
    parser.add_option('', '--port', metavar='port', default=5672, type='int', help='rabbitmq port, default: %default')
    parser.add_option('', '--vhost', metavar='vhost', default='/', help='rabbitmq vhost, default: %default')
    parser.add_option('', '--user', metavar='user', default='guest', help='rabbitmq user, default: %default')
    parser.add_option('', '--password', metavar='password', default='guest', help='rabbitmq password, default: %default')
    (options, args) = parser.parse_args()
    _run(options.host, options.port, options.vhost, options.user, options.password)

if __name__ == '__main__':
    main()
