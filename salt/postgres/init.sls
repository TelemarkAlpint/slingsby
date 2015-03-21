{% set version = pillar.get('postgres.version', '9.1') %}

postgresql-server:
  file.managed:
    - name: /etc/postgresql/{{ version }}/main/pg_hba.conf
    - source: salt://postgres/pg_hba.conf
    - user: postgres
    - makedirs: True
    - group: postgres
    - mode: 640

  pkg.installed:
    - name: postgresql-{{ version }}

  service.running:
    - name: postgresql
    - require:
      - pkg: postgresql-server
    - watch:
      - file: postgresql-server
      - file: postgresql-config

  cmd.run:
    - name: /usr/lib/postgresql/{{ version }}/bin/initdb /var/lib/postgresql/{{ version }}/main
    - user: postgres
    - unless: test -d /var/lib/postgresql/{{ version }}/main
    - require:
      - pkg: postgresql-server


postgresql-config:
  file.managed:
    - name: /etc/postgresql/{{ version }}/main/postgresql.conf
    - source: salt://postgres/postgresql.conf
    - makedirs: True
    - template: jinja
    - context:
      version: {{ version }}
    - watch_in:
      - service: postgresql-server


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


slingsby-postgres:
  postgres_user.present:
    - name: slingsby
    - password: "{{ salt['pillar.get']('slingsby:db_password') }}"
    - refresh_password: True
    - require:
      - service: postgresql-server

  postgres_database.present:
    - name: slingsby_rel
    - owner: slingsby
    - require:
      - postgres_user: slingsby-postgres
