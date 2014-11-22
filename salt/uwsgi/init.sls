uwsgi-deps:
  pkg.installed:
    - pkgs:
      - python-dev
      - python-pip


uwsgi:
  pip.installed:
    - require:
      - pkg: uwsgi-deps

  file.managed:
    - name: /etc/init/uwsgi.conf
    - source: salt://uwsgi/uwsgi.conf
    - template: jinja

  service.running:
    - require:
      - pip: uwsgi
    - watch:
      - file: uwsgi
      - file: slingsby-uwsgi-conf


uwsgi-apps-dir:
  file.directory:
    - name: /opt/apps


uwsgi-log-dir:
  file.directory:
    - name: /var/log/uwsgi
    - user: root
    - group: www
    - mode: 775
