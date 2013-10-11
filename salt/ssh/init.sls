ssh:
  service.running:
    - watch:
       - file: sshd_conf

sshd_conf:
  file.managed:
    - name: /etc/ssh/sshd_config
    - source: salt://ssh/sshd_conf
    - template: jinja
