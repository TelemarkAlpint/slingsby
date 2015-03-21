{% set nginx = pillar.get('nginx', {}) %}
{% set version_specifier = nginx.get('version_specifier', '1.6.2 sha1=1a5458bc15acf90eea16353a1dd17285cf97ec35') %}
{% set version, checksum = version_specifier.split() %}
{% set home = nginx.get('home', '/usr/local/nginx') %}
{% set source = nginx.get('source_root', '/usr/local/src') -%}

{% set nginx_package = source + '/nginx-' + version + '.tar.gz' -%}
{% set nginx_home     = home + "/nginx-" + version -%}

{% set pcre_version_identifier = nginx.get('pcre_version_identifier', '8.36 sha256=ef833457de0c40e82f573e34528f43a751ff20257ad0e86d272ed5637eb845bb') %}
{% set pcre_version, pcre_source_hash = pcre_version_identifier.split() %}


get-nginx:
  pkg.installed:
    - names:
      - build-essential
      - libssl-dev

  file.managed:
    - name: {{ nginx_package }}
    - source: http://nginx.org/download/nginx-{{ version }}.tar.gz
    - source_hash: {{ checksum }}

  cmd.wait:
    - cwd: {{ source }}
    - name: tar -zxf {{ nginx_package }} -C {{ home }}
    - require:
      - pkg: get-nginx
      - file: {{ home }}
    - watch:
      - file: get-nginx


get-pcre-source:
    file.managed:
        - name: {{ source }}/pcre-{{ pcre_version }}.tar.bz2
        - source: http://downloads.sourceforge.net/sourceforge/pcre/pcre-{{ pcre_version }}.tar.bz2
        - source_hash: {{ pcre_source_hash }}

    cmd.wait:
        - name: tar xf pcre-{{ pcre_version }}.tar.bz2
        - cwd: {{ source }}
        - require:
            - file: nginx-home
        - watch:
            - file: get-pcre-source


nginx-home:
  file.directory:
    - name: {{ home }}
    - user: nginx
    - group: nginx
    - makedirs: True
    - mode: 0755
    - require:
      - user: nginx-systemuser


nginx:
  cmd.wait:
    - cwd: {{ nginx_home }}
    - name: ./configure --conf-path=/etc/nginx/nginx.conf
            --sbin-path=/usr/sbin/nginx
            --user=nginx
            --group=nginx
            --prefix=/usr/local/nginx
            --error-log-path=/var/log/nginx/error.log
            --pid-path=/var/run/nginx.pid
            --lock-path=/var/lock/nginx.lock
            --http-log-path=/var/log/nginx/access.log
            --http-client-body-temp-path={{ home }}/body
            --http-proxy-temp-path={{ home }}/proxy
            --http-fastcgi-temp-path={{ home }}/fastcgi
            --without-http_browser_module
            --without-http_empty_gif_module
            --without-http_scgi_module
            --without-http_split_clients_module
            --without-http_map_module
            --without-http_geo_module
            --without-http_userid_module
            --without-http_ssi_module
            --with-http_stub_status_module
            --with-pcre={{ source }}/pcre-{{ pcre_version }}
            --with-pcre-jit
            --with-ipv6
            --with-cc-opt='-g -O2 -fstack-protector-all --param=ssp-buffer-size=4 -Wformat -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2'
            --with-ld-opt='-Wl,-z,relro,-z,now -Wl,--as-needed'
            --with-http_ssl_module &&
            make -j2 && make install
    - watch:
      - cmd: get-nginx
      - cmd: get-pcre-source
    - watch_in:
      - service: nginx

  init_script.managed:
    - upstart: salt://nginx/nginx-upstart
    - sysvinit: salt://nginx/nginx-sysvinit

  service.running:
    - enable: True
    - require:
      - cmd: nginx
      - file: {{ home }}
      - file: nginx-default-site
      - file: nginx-sites-enabled
    - watch:
      - init_script: nginx
      - file: nginx-conf
