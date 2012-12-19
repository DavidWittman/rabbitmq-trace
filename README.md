rabbitmq trace scripts. test by Python 2.7.3 (pika 0.9.8) and RabbitMQ 3.0.0

Require:

    * pika (Python AMQP client library)https://github.com/pika/pika
    * rabbitmq_tracing (RabbitMQ plugin)

Install:

    $ sudo pip install pika
    $ sudo rabbitmq-plugins enable rabbitmq_tracing

Usage:

    $ sudo rabbitmqctl trace_on
    $ ./rabbitmqtrace.py
    << output >>
