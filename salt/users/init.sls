# Make sure the admin group is present
admin-group:
    group.present:
        - name: admin
        - order: 1
        - system: True


{% for username, user in salt['pillar.get']('developers', {}).items() %}
{{ username }}:
  user.present:
    - fullname: {{ user['fullname'] }}
    - shell: {{ user.get('shell', '/bin/bash') }}
    - groups:
      {% for group in user['groups'] %}
        - {{ group }}
      {% endfor %}
    {% if 'password_pillar' in user %}
    - password: "{{ pillar[user['password_pillar']] }}"
    {% endif %}

  {% if 'ssh_keys' in user %}
  ssh_auth.present:
    - user: {{ username }}
    - require:
      - user: {{ username }}
    - names:
      {% for ssh_key in user['ssh_keys'] %}
      - {{ ssh_key }}
      {% endfor %}
  {% endif %}
{% endfor %}


{% for absent_user in pillar.get('absent_users', []) %}
{{ absent_user }}:
  user.absent:
    - purge: True
    - force: True
{% endfor %}
