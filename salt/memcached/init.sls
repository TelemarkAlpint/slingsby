memcached:
  pkg:
    pkgs:
      - memcached
      - libmemcached-dev # needed to compile pylibmc

  file.managed:
    - name: /etc/memcached.conf
    - source: salt://memcached/memcached.conf

  service.running:
    - require:
      - pkg: memcached
    - watch:
      - file: memcached

  user.present:
    - fullname: memcached worker
    - system: True
    - createhome: False
    - shell: /usr/sbin/nologin
