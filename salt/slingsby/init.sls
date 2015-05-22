# Actual code deployed by Travis and fabric, just set up the virtualenv and the directories needed

{% set requirements_files = ['prod-requirements.txt', 'requirements.txt'] %}

include:
  - memcached
  - mysql
  - nginx
  - rabbitmq


slingsby-deps:
  pkg.installed:
    - pkgs:
      - lame
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
  user.present:
    - system: True
    - shell: /usr/sbin/nologin
    - createhome: False
    - fullname: slingsby worker
    - groups:
      - memcached

  init_script.managed:
    - upstart: salt://slingsby/slingsby-upstart
    - sysvinit: salt://slingsby/slingsby-sysvinit

  service.running:
    - enable: True
    - watch:
      - init_script: slingsby

  virtualenv.managed:
    - name: /srv/ntnuita.no/venv
    - requirements: /srv/ntnuita.no/prod-requirements.txt
    - no_deps: True
    - require:
      - pkg: slingsby-deps
      - pkg: mysql
      {% for req_file in requirements_files %}
      - file: slingsby-requirements-{{ req_file }}
      {% endfor %}

  file.managed:
    - name: /srv/ntnuita.no/prod_settings.py
    - source: salt://slingsby/prod_settings.py
    - template: jinja
    - show_diff: False
    - user: root
    - group: slingsby
    - mode: 640
    - require:
      - virtualenv: slingsby
      - user: slingsby
    - watch_in:
      - serivce: slingsby


slingsby-log-dir:
  file.directory:
    - name: /var/log/slingsby
    - makedirs: True
    - user: root
    - group: slingsby
    - mode: 775
    - require:
      - user: slingsby


slingsby-static-dir:
  file.directory:
    - name: /srv/ntnuita.no/static
    - makedirs: True
    - user: root
    - group: slingsby
    - mode: 755
    - require:
      - user: slingsby


slingsby-media-dir:
  file.directory:
    - name: /srv/ntnuita.no/media
    - makedirs: True
    - user: root
    - group: slingsby
    - mode: 775
    - require:
      - user: slingsby


slingsby-celery:
  init_script.managed:
    - upstart: salt://slingsby/celery_job_conf-upstart
    - sysvinit: salt://slingsby/celery_job_conf-sysvinit

  service.running:
    - enable: True
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


# Fix a bug in djecelery/mysql where index keys can't be longer than some arbitrary mysql limit
{% for dir in ('', 'local/') %}
djcelery-mysql-fix{{ dir }}:
  file.replace:
    - name: /srv/ntnuita.no/venv/{{ dir }}lib/python2.7/site-packages/djcelery/models.py
    - pattern: max_length=2\d\d
    - repl: max_length=191
    - onlyif: test -f /srv/ntnuita.no/venv/{{ dir }}lib/python2.7/site-packages/djcelery/models.py
    - watch:
      - virtualenv: slingsby
{% endfor %}
