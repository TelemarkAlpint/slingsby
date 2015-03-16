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
