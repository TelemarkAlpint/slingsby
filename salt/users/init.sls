{% for username, user in salt['pillar.get']('developers', {}).items() %}
{{ username }}:
  user.present:
    - fullname: {{ user['fullname'] }}
    - shell: {{ user.get('shell', '/bin/bash') }}
    - groups:
      {% for group in user['groups'] %}
        - {{ group }}
      {% endfor %}

  ssh_auth.present:
    - user: {{ username }}
    - require:
      - user: {{ username }}
    - names:
      {% for ssh_key in user['ssh_keys'] %}
      - {{ ssh_key }}
      {% endfor %}
{% endfor %}



{% for absent_user in pillar.get('absent_users', []) %}
{{ absent_user }}:
  user.absent:
    - purge: True
    - force: True
{% endfor %}



{% for daemon_user, daemon_fullname in pillar.get('daemon_users', {}).items() %}
{{ daemon_user }}:
  user.present:
    - order: 1
    - fullname: {{ daemon_fullname }}
    - createhome: False
    - system: True
    - shell: /usr/sbin/nologin
    - home: /nonexistent
{% endfor %}
