newrelic:
  pip.installed:
    - require:
      - pkg: python-pip

newrelic_conf:
  file.managed:
    - name: /etc/newrelic.ini
    - source: salt://newrelic/newrelic.ini
    - template: jinja
    - show_diff: False
    - require:
      - pip: newrelic
