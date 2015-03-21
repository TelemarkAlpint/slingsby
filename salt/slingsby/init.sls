# Actual code deployed by Travis and fabric, just set up the virtualenv and the directories needed

{% set requirements_files = ['prod-requirements.txt', 'requirements.txt'] %}

include:
  - .cron
  - memcached
  - nginx
  - rabbitmq
  - uwsgi


slingsby-deps:
  pkg.installed:
    - pkgs:
      - lame
      - libpq-dev
      - libjpeg-dev # Needed for PIL to decode JPEGs
      - python-dev # required for db bindings to compile
      - python-pip
      - python-virtualenv
      - sox

{% for req_file in requirements_files %}
slingsby-requirements-{{ req_file }}:
  file.managed:
    - name: /srv/ntnuita.no/{{ req_file }}
    - source: salt://slingsby/{{ req_file }}
    - makedirs: True
{% endfor %}

slingsby:
  virtualenv.managed:
    - name: /srv/ntnuita.no/venv
    - requirements: /srv/ntnuita.no/prod-requirements.txt
    - no_deps: True
    - require:
      - pkg: slingsby-deps
      {% for req_file in requirements_files %}
      - file: slingsby-requirements-{{ req_file }}
      {% endfor %}

  file.managed:
    - name: /srv/ntnuita.no/prod_settings.py
    - source: salt://slingsby/prod_settings.py
    - template: jinja
    - show_diff: False
    - user: root
    - group: uwsgi
    - mode: 640
    - require:
      - virtualenv: slingsby
      - user: uwsgi-user
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
    - group: uwsgi
    - mode: 775
    - require:
      - user: uwsgi-user


slingsby-static-dir:
  file.directory:
    - name: /srv/ntnuita.no/static
    - makedirs: True
    - user: root
    - group: uwsgi
    - mode: 755
    - require:
      - user: uwsgi-user


slingsby-media-dir:
  file.directory:
    - name: /srv/ntnuita.no/media
    - makedirs: True
    - user: root
    - group: uwsgi
    - mode: 775
    - require:
      - user: uwsgi-user


slingsby-celery:
  init_script.managed:
    - upstart: salt://slingsby/celery_job_conf-upstart
    - sysvinit: salt://slingsby/celery_job_conf-sysvinit

  service.running:
    - watch:
      - init_script: slingsby-celery
      - file: slingsby


slingsby-nginx-site:
  file.managed:
    - name: /etc/nginx/sites-enabled/slingsby
    - source: salt://slingsby/slingsby-nginx-site
    - template: jinja
    - require:
      - cmd: nginx
    - watch_in:
      - service: nginx
