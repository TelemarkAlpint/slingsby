# required to compile uwsgi
python-dev:
  pkg.installed


uwsgi:
  pip.installed:
    - require:
      - pkg: python-pip
      - pkg: python-dev

  service.running:
    - require:
      - pip: uwsgi
    - watch:
      - file: newrelic_conf
      - file: uwsgi_conf
      - file: slingsby_settings
      - file: slingsby_uwsgi_conf


uwsgi_conf:
  file.managed:
    - name: /etc/init/uwsgi.conf
    - source: salt://uwsgi/uwsgi.conf


log_dir:
  file.directory:
    - name: /var/log/uwsgi
    - user: www
    - group: www
    - mode: 644
