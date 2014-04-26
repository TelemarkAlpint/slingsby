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
      - file: sites_available


# For the pre-config loaded directory
nginx_log_dir:
  file.directory:
    - name: /usr/share/nginx/logs
    - user: root
    - group: www
    - mode: 770


nginx-sites-enabled:
  file.recurse:
    - name: /etc/nginx/sites-enabled
    - source: salt://nginx/sites-enabled


# Disable default
nginx-default-site:
  file.absent:
    - name: /etc/nginx/sites-enabled/default
