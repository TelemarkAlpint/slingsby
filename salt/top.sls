base:
  '*':
    - memcached
    - mysql
    - ntp
    - nginx
    - pip
    - pkg
    - rabbitmq
    - slingsby
    - users
    - uwsgi

  'ntnuita.no':
    - newrelic
    - ssh

  'vagrant':
    - mysql.server
