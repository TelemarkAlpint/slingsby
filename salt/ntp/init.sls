ntp:
  pkg:
    - installed

  service.running:
    - require:
      - pkg: ntp
    - watch:
      - file: ntp_config


ntp_config:
  file.managed:
    - name: /etc/ntp.conf
    - source: salt://ntp/ntp_config
