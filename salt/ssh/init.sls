ssh:
  file.managed:
    - name: /etc/ssh/.sshd_config_candidate
    - source: salt://ssh/sshd_conf
    - template: jinja

  cmd.wait:
    - name: sshd -f /etc/ssh/.sshd_config_candidate -t && cp /etc/ssh/.sshd_config_candidate /etc/ssh/sshd_config
    - watch:
      - file: ssh

  service.running:
    - watch:
       - cmd: ssh
