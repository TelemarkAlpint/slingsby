newrelic:
  pip.installed:
    - require:
      - pkg: python-pip

  file.managed:
    - name: /etc/newrelic.ini
    - source: salt://newrelic/newrelic.ini
    - template: jinja
    - show_diff: False
    - user: root
    - group: www
    - mode: 640
    - require:
      - pip: newrelic
    - watch_in:
      - service: uwsgi
