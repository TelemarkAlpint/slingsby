nginx:
  pkgrepo.managed:
   - ppa: nginx/stable
  pkg:
    - installed
    - require:
      - pkgrepo: nginx
  service:
    - running
    - require:
      - pkg: nginx
    - watch:
      - file: nginx_conf

nginx_conf:
  file.managed:
    - name: /etc/nginx/nginx.conf
    - source: salt://nginx/nginx.conf
    - mode: 644
    - user: root
    - group: root

# For the pre-config loaded directory
nginx_log_dir:
  file.directory:
    - name: /usr/share/nginx/logs
    - user: root
    - group: root
    - mode: 740

sites_available:
  file.recurse:
    - name: /etc/nginx/sites-available
    - source: salt://nginx/sites-available



# Enabled sites:
slingsby:
  file.symlink:
    - name: /etc/nginx/sites-enabled/slingsby
    - target: /etc/nginx/sites-available/slingsby

# Disable default
default:
  file.absent:
    - name: /etc/nginx/sites-enabled/default
