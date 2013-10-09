venv:
  pip.installed:
    - name: virtualenv
    - require:
      - pkg: python-pip

  file.directory:
    - name: /srv/ntnuita.no/venv
    - makedirs: True
    - user: www
    - group: www

  virtualenv.managed:
    - name: /srv/ntnuita.no/venv
    - require:
      - pip: virtualenv
      - file: /srv/ntnuita.no/venv
      - pkg: python-dev # required for psycopg2 to compile


slingsby_uwsgi_conf:
  file.managed:
    - name: /srv/ntnuita.no/uwsgi.ini
    - source: salt://slingsby/uwsgi_conf
    - mode: 444
    - user: www
    - group: www


slingsby_settings:
  file.managed:
    - name: /srv/ntnuita.no/prod_settings.py
    - source: salt://slingsby/prod_settings.py
    - template: jinja
    - show_diff: False

postgres:
  postgres_user.present:
    - name: slingsby

  postgres_database.present:
    - name: slingsby_rel

  # Sync db
  cmd.run:
    - cwd: /srv/ntnuita.no
    - name: ./venv/bin/manage.py syncdb --noinput --settings prod_settings
    # Only sync if slingsby has been installed (ie not first provision run)
    - onlyif: test -f ./venv/bin/manage.py
    - env:
      - PYTHONPATH: /srv/ntnuita.no
    - user: root
    - require:
      - file: slingsby_settings


slingsby_log_dir:
  file.directory:
    - name: /var/log/slingsby
    - user: www
    - group: www
