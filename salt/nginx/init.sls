{% set old_sites = pillar.get('old_sites', []) %}

nginx:
  pkgrepo.managed:
    {% if grains['lsb_distrib_codename'] == 'wheezy' %}
    # We're on the rasbian server, no ppa support
    - name: deb http://nginx.org/packages/debian wheezy nginx
    - keyid: ABF5BD827BD9BF62
    - keyserver: keyserver.ubuntu.com
    {% else %}
    - ppa: nginx/stable
    {% endif %}

  pkg.installed:
    - name: nginx-light
    - require:
      - pkgrepo: nginx
      - user: nginx

  file.managed:
    - name: /etc/nginx/nginx.conf
    - source: salt://nginx/nginx.conf
    - mode: 644
    - user: root
    - group: root
    - require:
      - pkg: nginx
      - user: nginx

  service.running:
    - watch:
      - file: nginx
      - file: nginx-default-site

  user.present:
    - name: nginx
    - systemuser: True
    - fullname: Nginx worker
    - createhome: False
    - shell: /usr/sbin/nologin
    - home: /nonexistent

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
      - pkg: nginx
