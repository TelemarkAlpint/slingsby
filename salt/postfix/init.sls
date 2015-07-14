{% set postfix = pillar.get('postfix', {}) -%}

postfix:
  pkg.installed:
    - pkgs:
        - postfix

  file.managed:
    - name: /etc/postfix/main.cf
    - source: salt://postfix/main.cf
    - template: jinja

  service.running:
    - enable: True
    - require:
      - pkg: postfix
    - watch:
      - file: postfix


postfix-master-config:
    file.managed:
        - name: /etc/postfix/master.cf
        - source: salt://postfix/master.cf
        - watch_in:
            - service: postfix


{% if grains['id'] == 'vagrant' %}
local-redirect:
  file.managed:
    - name: /etc/postfix/canonical-redirect
    - contents: /^.*$/ root
    - watch_in:
      - service: postfix
{% endif %}
