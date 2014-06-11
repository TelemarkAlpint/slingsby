memcached:
  pkg:
    - installed

  file.managed:
    - name: /etc/memcached.conf
    - source: salt://memcached/memcached.conf

  service.running:
    - require:
      - pkg: memcached
    - watch:
      - file: memcached
