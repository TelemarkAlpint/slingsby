# Actual code deployed by Travis and fabric, just set up the virtualenv and the directories needed

include:
  - .cron

slingsby-deps:
  pip.installed:
    - name: virtualenv

  pkg.installed:
    - pkgs:
      - lame
      - sox

slingsby:
  virtualenv.managed:
    - name: /srv/ntnuita.no/venv
    - requirements: salt://slingsby/prod-requirements.txt
    - require:
      - pip: slingsby-deps
      - pkg: python-dev # required for db bindings to compile
      - pkg: mysql # Needed to compile db bindings

  file.managed:
    - name: /srv/ntnuita.no/prod_settings.py
    - source: salt://slingsby/prod_settings.py
    - template: jinja
    - show_diff: False
    - user: root
    - group: www
    - mode: 640
    - require:
      - virtualenv: slingsby
    - watch_in:
      - service: uwsgi


slingsby-uwsgi-conf:
  file.managed:
    - name: /opt/apps/slingsby.ini
    - source: salt://slingsby/uwsgi_conf
    - makedirs: True


slingsby-log-dir:
  file.directory:
    - name: /var/log/slingsby
    - makedirs: True
    - user: root
    - group: www
    - mode: 775


slingsby-static-dir:
  file.directory:
    - name: /srv/ntnuita.no/static
    - makedirs: True
    - user: root
    - group: www
    - mode: 755


slingsby-media-dir:
  file.directory:
    - name: /srv/ntnuita.no/media
    - makedirs: True
    - user: root
    - group: www
    - mode: 775


slingsby-celery:
  file.managed:
    - name: /etc/init/slingsby-celery.conf
    - source: salt://slingsby/celery_job_conf

  service.running:
    - watch:
      - file: slingsby-celery
