# required to compile uwsgi
python-dev:
  pkg.installed


uwsgi:
  pip.installed:
    - require:
      - pkg: python-pip
      - pkg: python-dev

  file.managed:
    - name: /etc/init/uwsgi.conf
    - source: salt://uwsgi/uwsgi.conf
    - template: jinja

  service.running:
    - require:
      - pip: uwsgi
    - watch:
      - file: uwsgi
      - file: slingsby_uwsgi_conf


log_dir:
  file.directory:
    - name: /var/log/uwsgi
    - user: root
    - group: www
    - mode: 775
