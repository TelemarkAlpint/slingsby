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
    - sudo
    - users
    - uwsgi

  'ntnuita.no':
    - newrelic
    - ssh

  'vagrant':
    - mysql.server
