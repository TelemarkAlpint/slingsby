{% set version = pillar.get('postgres.version', '9.4') %}

postgresql-server:
  pkgrepo.managed:
    - humanname: PostgreSQL repo
    - name: deb http://apt.postgresql.org/pub/repos/apt/ {{ grains['lsb_distrib_codename'] }}-pgdg main
    - key_url: https://www.postgresql.org/media/keys/ACCC4CF8.asc

  pkg.installed:
    - name: postgresql-{{ version }}
    - require:
      - pkgrepo: postgresql-server

  file.managed:
    - name: /etc/postgresql/{{ version }}/main/pg_hba.conf
    - source: salt://postgres/pg_hba.conf
    - user: postgres
    - group: postgres
    - mode: 640
    - require:
      - pkg: postgresql-server

  service.running:
    - name: postgresql
    - require:
      - pkg: postgresql-server
    - watch:
      - file: postgresql-server


postgresql-config:
  file.managed:
    - name: /etc/postgresql/{{ version }}/main/postgresql.conf
    - source: salt://postgres/postgresql.conf
    - require:
      - pkg: postgresql-server
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
