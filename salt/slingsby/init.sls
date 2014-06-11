# Actual code deployed by Travis and fabric, just set up the virtualenv and the directories needed

include:
  - .cron

virtualenv:
  pip.installed

slingsby:
  virtualenv.managed:
    - name: /srv/ntnuita.no/venv
    - requirements: salt://slingsby/prod-requirements.txt
    - require:
      - pip: virtualenv
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

slingsby_uwsgi_conf:
  file.managed:
    - name: /srv/ntnuita.no/uwsgi.ini
    - source: salt://slingsby/uwsgi_conf
    - mode: 444
    - require:
      - virtualenv: slingsby


slingsby_log_dir:
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
