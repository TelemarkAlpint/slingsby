{% set version = pillar.get('postgres.version', '9.4') %}
{% set install_from_source = pillar.get('postgres.install_from_source', True) %}
{% set postgres_server_type = 'cmd' if install_from_source else 'pkg' %}

include:
{% if install_from_source %}
  - .source
{% else %}
  - .pkg
{% endif %}


postgresql-server-common:
  file.managed:
    - name: /etc/postgresql/{{ version }}/main/pg_hba.conf
    - source: salt://postgres/pg_hba.conf
    - user: postgres
    - group: postgres
    - mode: 640
    - require:
      - {{ postgres_server_type }}: postgresql-server

  service.running:
    - name: postgresql
    - require:
      - {{ postgres_server_type }}: postgresql-server
    - watch:
      - file: postgresql-server-common
      - file: postgresql-config


postgresql-config:
  file.managed:
    - name: /etc/postgresql/{{ version }}/main/postgresql.conf
    - source: salt://postgres/postgresql.conf
    - require:
      - {{ postgres_server_type }}: postgresql-server


# Create on-disk dumps of the postgres db so that it can be backed up by other utilities
# (the on-disk pg format is not reliable for backup unless you can take atomic snapshots,
# which we can't guarantee unless we're using btrfs or zfs to do the backup)
postgresql-server-backups:
    file.directory:
        - name: /var/backups/postgres
        - user: root
        - group: postgres
        - mode: 775

    cron.present:
        - name: cd /tmp; sudo -u postgres pg_dumpall | gzip > /var/backups/postgres/dump.sql.gz
        - identifier: postgresql-server-backups
        - minute: random
        - hour: '*/4'


postgresql-client:
  pkg.installed:
    - pkgs:
      - postgresql-client-common
      - postgresql-client-{{ version }}


slingsby-postgres:
  postgres_user.present:
    - name: slingsby
    - password: "{{ salt['pillar.get']('slingsby:db_password') }}"
    - refresh_password: True
    - require:
      - pkg: postgresql-client

  postgres_database.present:
    - name: slingsby_rel
    - owner: slingsby
    - require:
      - postgres_user: slingsby-postgres
