RabbitMQ trace scripts. test by Python 2.7.3 (pika 0.9.8) and RabbitMQ 3.0.0

*warning: trace just for debug RabbitMQ*

Require:

    * pika (Python AMQP client library) https://github.com/pika/pika
    * rabbitmq_tracing (RabbitMQ plugin)

Install:

    $ sudo pip install pika
    $ sudo rabbitmq-plugins enable rabbitmq_tracing

Example:

    $ sudo rabbitmqctl trace_on
    $ ./rabbitmqtrace.py
    << output >>

Usage:

    $ ./rabbitmqtrace.py --help
    Usage: rabbitmqtrace.py

    Options:
      -h, --help           show this help message and exit
      --host=host          rabbitmq host address, default: localhost
      --port=port          rabbitmq port, default: 5672
      --vhost=vhost        rabbitmq vhost, default: /
      --user=user          rabbitmq user, default: guest
      --password=password  rabbitmq password, default: guest

__END__
