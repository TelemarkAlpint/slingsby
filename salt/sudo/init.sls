sudoers:
  file.managed:
    - name: /etc/sudoers
    - source: salt://sudo/sudoers
    - mode: 440
    - user: root
    - group: root
