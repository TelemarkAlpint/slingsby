# Binary releases of postgres for armhf platforms (ie raspbian) are not available, thus
# we compile from source on those

{% set postgres = pillar.get('postgres', {}) %}
{% set version = postgres.get('version_specifier', '9.4.1') %}

postgres-deps:
  pkg.installed:
    - pkgs:
      - libreadline-dev

postgres-source:
  file.managed:
    - name: /usr/local/src/postgresql-{{ version }}.tar.bz2
    - source: https://ftp.postgresql.org/pub/source/v{{ version }}/postgresql-{{ version }}.tar.bz2
    - source_hash: https://ftp.postgresql.org/pub/source/v{{ version }}/postgresql-{{ version }}.tar.bz2.sha256

  cmd.wait:
    - name: tar xfo postgresql-{{ version }}.tar.bz2 --no-same-permissions
    - cwd: /usr/local/src
    - watch:
      - file: postgres-source


postgresql-server:
  cmd.wait:
    - name: ./configure &&
            make && make install
    - cwd: /usr/local/src/postgresql-{{ version }}
    - require:
      - pkg: postgres-deps
    - watch:
      - cmd: postgres-source
