rabbitmq-deps:
  pkg.installed:
    - pkgs:
      - apt-transport-https

rabbitmq:
  pkgrepo.managed:
    - humanname: RabbitMQ Debian repo
    - name: deb https://www.rabbitmq.com/debian/ testing main
    - key_url: https://www.rabbitmq.com/rabbitmq-signing-key-public.asc
    - require:
      - pkg: rabbitmq-deps

  pkg.installed:
    - name: rabbitmq-server
    - require:
      - pkgrepo: rabbitmq
      {% if grains['id'] == 'vagrant' %}
      - cmd: hostname
      {% endif %}

  service.running:
    - name: rabbitmq-server
    - require:
      - pkg: rabbitmq
