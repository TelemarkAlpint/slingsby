base:
  '*':
    - memcached
    - mysql
    - ntp
    - nginx
    - old-sites
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
