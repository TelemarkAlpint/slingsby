{% set old_sites = pillar.get('old_sites', []) %}

nginx:
  pkgrepo.managed:
   - ppa: nginx/stable

  pkg.installed:
    - require:
      - pkgrepo: nginx

  file.managed:
    - name: /etc/nginx/nginx.conf
    - source: salt://nginx/nginx.conf
    - mode: 644
    - user: root
    - group: www
    - require:
      - pkg: nginx

  service.running:
      - service: uwsgi
    - watch:
      - file: nginx
      - file: slingsby-site


# Make sure nginx log dir has correct users and permissions
nginx-log-dir:
  file.directory:
    - name: /var/log/nginx
    - user: root
    - group: www
    - mode: 775


slingsby-site:
  file.managed:
    - name: /etc/nginx/sites-enabled/slingsby
    - source: salt://nginx/sites-enabled/slingsby
    - template: jinja
    - require:
      - file: nginx-default-site
    - watch_in:
      - service: nginx

{% for old_site in old_sites %}
{{ old_site }}-site:
  file.managed:
    - name: /etc/nginx/sites-enabled/{{ old_site }}
    - source: salt://nginx/sites-enabled/old-site
    - template: jinja
    - context:
      year: {{ old_site }}
    - watch_in:
      - service: nginx
{% endfor %}


# Disable default
nginx-default-site:
  file.absent:
    - name: /etc/nginx/sites-enabled/default
    - require:
      - pkg: nginx
