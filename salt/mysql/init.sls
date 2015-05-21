mysql:
  pkg.installed:
    - pkgs:
      - libmysqlclient-dev
      - mysql-client-5.5
    - skip_verify: True
