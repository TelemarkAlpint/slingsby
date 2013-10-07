postgresql:
  pkg.installed:
    - pkgs:
      - postgresql
      - libpq-dev

  service.running:
    - require:
      - pkg: postgresql
    - watch:
      - file: pg_config

pg_config:
  file.managed:
    - name: /etc/postgresql/9.1/main/pg_hba.conf
    - source: salt://postgres/pg_hba.conf
