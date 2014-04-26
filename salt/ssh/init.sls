ssh:
  file.managed:
    - name: /etc/ssh/sshd_config
    - source: salt://ssh/sshd_conf
    - template: jinja

  service.running:
    - watch:
       - file: sshd
