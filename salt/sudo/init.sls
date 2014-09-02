sudoers:
    file.managed:
        - name: /etc/sudoers-candidate
        - source: salt://sudo/sudoers
        - template: jinja
        - mode: 440
        - user: root
        - group: root

    cmd.wait:
        - name: visudo -cf /etc/sudoers-candidate && cp /etc/sudoers-candidate /etc/sudoers
        - watch:
            - file: sudoers
