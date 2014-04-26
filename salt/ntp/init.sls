ntp:
  pkg:
    - installed

  file.managed:
    - name: /etc/ntp.conf
    - source: salt://ntp/ntp_config

  service.running:
    - require:
      - pkg: ntp
    - watch:
      - file: ntp


