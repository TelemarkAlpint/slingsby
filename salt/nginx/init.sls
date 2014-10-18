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
    - require:
      - file: nginx_log_dir
      - service: uwsgi
    - watch:
      - file: nginx
      - file: slingsby-site


# For the pre-config loaded directory
nginx_log_dir:
  file.directory:
    - name: /usr/share/nginx/logs
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


2004-site:
  file.managed:
    - name: /etc/nginx/sites-enabled/2004
    - source: salt://nginx/sites-enabled/2004
    - template: jinja
    - watch_in:
      - service: nginx


# Disable default
nginx-default-site:
  file.absent:
    - name: /etc/nginx/sites-enabled/default
    - require:
      - pkg: nginx
