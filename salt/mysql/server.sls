{% set slingsby = pillar.get('slingsby', {}) -%}

mysql-deps:
  pkg.installed:
    - name: python-mysqldb # Needed for salt to manage db users/grants etc

  # Needed to prevent page allocation failures on vagrant
  file.append:
    - name: /etc/sysctl.conf
    - text: vm.min_free_kbytes=65536


mysql-server:
  pkg.installed:
    - name: mysql-server-5.5
    - require:
      - pkg: mysql-deps

  file.managed:
    - name: /etc/mysql/my.cnf
    - source: salt://mysql/my.cnf

  service.running:
    - name: mysql
    - require:
      - file: mysql-deps
      - pkg: mysql-server
    - watch:
      - file: mysql-server


slingsby-db:
  mysql_database.present:
    - name: telemark_slingsby
    - character_set: utf8mb4
    - require:
      - service: mysql-server

  mysql_user.present:
    - name: telemark_dbadmin
    - host: ntnuita.local
    - password: "{{ slingsby.db_password }}"
    - require:
      - service: mysql-server

  mysql_grants.present:
    - grant: all
    - user: telemark_dbadmin
    - host: ntnuita.local
    - database: telemark_slingsby.*
    - require:
      - mysql_database: slingsby-db
      - mysql_user: slingsby-db


mysql-firewall:
  iptables.append:
    - table: filter
    - chain: INPUT
    - match:
      - comment
    - comment: "mysql.server: Allow incoming MySQL connections"
    - proto: tcp
    - dport: 3306
    - jump: ACCEPT
    - save: True
