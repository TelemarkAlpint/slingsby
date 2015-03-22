{% set old_sites = pillar.get('old_sites', []) %}
{% set nginx = pillar.get('nginx', {}) %}


nginx-systemuser:
  user.present:
    - name: nginx
    - fullname: nginx worker
    - system: True
    - createhome: False
    - shell: /usr/sbin/nologin
    - groups:
        - shadow
    - optional_groups:
        - phpworker


include:
  - nginx.source

nginx-conf:
  file.managed:
    - name: /etc/nginx/nginx.conf
    - source: salt://nginx/nginx.conf
    - template: jinja
    - mode: 640
    - user: root
    - group: nginx
    - require:
      - cmd: nginx
      - user: nginx-systemuser
    - watch_in:
      - service: nginx


# Make sure nginx log dir has correct users and permissions
nginx-log-dir:
  file.directory:
    - name: /var/log/nginx
    - user: root
    - group: nginx
    - mode: 775


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
      - cmd: nginx


nginx-sites-enabled:
  file.directory:
    - name: /etc/nginx/sites-enabled
    - user: root
    - group: nginx
    - mode: 755
    - require:
      - file: nginx-conf
      - user: nginx-systemuser

nginx-proxy-params:
  file.managed:
    - name: /etc/nginx/proxy_params
    - source: salt://nginx/proxy_params
    - require:
      - file: nginx-conf
    - watch_in:
      - service: nginx
