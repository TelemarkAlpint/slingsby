rabbitmq:
  pkgrepo.managed:
    - humanname: RabbitMQ Debian repo
    - name: deb https://www.rabbitmq.com/debian/ testing main
    - key_url: https://www.rabbitmq.com/rabbitmq-signing-key-public.asc

  pkg.installed:
    - name: rabbitmq-server
    - require:
      - pkgrepo: rabbitmq

  service.running:
    - name: rabbitmq-server
    - require:
      - pkg: rabbitmq
