memcached:
  pkg:
    - installed

  service:
    - running
    - require:
      - pkg: memcached
    - watch:
      - file: memcached_config

memcached_config:
  file.managed:
    - name: /etc/memcached.conf
    - source: salt://memcached/memcached.conf
