{% set slingsby = pillar.get('slingsby', {}) -%}

mysql-deps:
  pkg.installed:
    - name: python-mysqldb

  # Needed to prevent page allocation failures on vagrant
  file.append:
    - name: /etc/sysctl.conf
    - text: vm.min_free_kbytes=65536


mysql-server:
  pkg.installed:
    - name: mysql-server-5.6
    - skip_verify: True
    - require:
      - pkg: mysql-deps

  service.running:
    - name: mysql
    - require:
      - file: mysql-deps
      - pkg: mysql-server


slingsby-db:
  mysql_database.present:
    - name: slingsby_rel
    - character_set: utf8mb4
    - require:
      - service: mysql-server

  mysql_user.present:
    - name: slingsby
    - password: "{{ slingsby.db_password }}"
    - require:
      - service: mysql-server

  mysql_grants.present:
    - grant: all
    - user: slingsby
    - database: slingsby_rel.*
    - require:
      - mysql_database: slingsby-db
      - mysql_user: slingsby-db
