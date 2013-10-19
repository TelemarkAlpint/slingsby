mysql:
  pkgrepo.managed:
    - ppa: ondrej/mysql-5.6

  pkg.installed:
    - pkgs:
      - libmysqlclient-dev
      - mysql-client-5.6
    - skip_verify: True
    - require:
      - pkgrepo: mysql
