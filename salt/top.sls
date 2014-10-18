base:
  '*':
    - memcached
    - mysql
    - ntp
    - nginx
    - old-sites
    - pip
    - pkg
    - rabbitmq
    - slingsby
    - sudo
    - users
    - uwsgi

  'ntnuita.no':
    - ssh

  'vagrant':
    - mysql.server
