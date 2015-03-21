uwsgi-user:
  user.present:
    - name: uwsgi
    - fullname: uWSGI worker
    - system: True
    - createhome: False
    - shell: /usr/sbin/nologin
    - home: /nonexistent


uwsgi-deps:
  pkg.installed:
    - pkgs:
      - python-dev
      - python-pip


uwsgi:
  pip.installed:
    - require:
      - pkg: uwsgi-deps

  init_script.managed:
    - upstart: salt://uwsgi/uwsgi-upstart
    - sysvinit: salt://uwsgi/uwsgi-sysvinit

  service.running:
    - require:
      - pip: uwsgi
      - user: uwsgi-user
      - file: uwsgi-log-dir
    - watch:
      - init_script: uwsgi
      - file: slingsby-uwsgi-conf


uwsgi-apps-dir:
  file.directory:
    - name: /opt/apps


uwsgi-log-dir:
  file.directory:
    - name: /var/log/uwsgi
    - user: root
    - group: uwsgi
    - mode: 775
    - require:
      - user: uwsgi-user
