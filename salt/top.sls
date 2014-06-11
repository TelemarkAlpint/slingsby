base:
  '*':
    - memcached
    - mysql
    - ntp
    - nginx
    - pip
    - pkg
    - slingsby
    - users
    - uwsgi

  'ntnuita.no':
    - newrelic
    - ssh

  'vagrant':
    - mysql.server
