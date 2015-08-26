# Sanity-check the pillar data before execution
include:
    - .pillar_check

opendkim:
    pkg.installed:
        - pkgs:
            - opendkim
            - opendkim-tools

    file.managed:
        - name: /etc/opendkim.conf
        - source: salt://opendkim/opendkim.conf

    service.running:
        - watch:
            - file: opendkim


opendkim-dir:
    file.directory:
        - name: /etc/opendkim


opendkim-key-dir:
    file.directory:
        - name: /etc/opendkim/keys
        - user: root
        - group: opendkim
        - mode: 750
        - require:
            - file: opendkim-dir


opendkim-trusted-hosts:
    file.managed:
        - name: /etc/opendkim/TrustedHosts
        - contents: |
            127.0.0.1
            localhost
            192.168.0.1/24
            {% for domain in pillar.get('opendkim', {}).keys() %}
            {{ domain }}
            {%- endfor %}
        - require:
            - file: opendkim-dir
        - watch_in:
            - service: opendkim


opendkim-key-table:
    file.managed:
        - name: /etc/opendkim/KeyTable
        - contents: |
            {% for domain, selector in pillar.get('opendkim', {}).iteritems() -%}
            {{ selector }}._domainkey.{{ domain }} {{ domain }}:{{ selector }}:/etc/opendkim/keys/{{ domain }}/{{ selector }}.private
            {%- endfor %}
        - require:
            - file: opendkim-dir
        - watch_in:
            - service: opendkim


opendkim-signing-table:
    file.managed:
        - name: /etc/opendkim/SigningTable
        - contents: |
            {% for domain, selector in pillar.get('opendkim', {}).iteritems() -%}
            *@{{ domain }} {{ selector }}._domainkey.{{ domain }}
            {%- endfor %}
        - require:
            - file: opendkim-dir
        - watch_in:
            - service: opendkim


{% for domain, selector in pillar.get('opendkim', {}).iteritems() %}
opendkim-host-key-dir-{{ domain }}:
    file.directory:
        - name: /etc/opendkim/keys/{{ domain }}
        - user: root
        - group: opendkim
        - mode: 750
        - require:
            - file: opendkim-key-dir


opendkim-remove-old-host-key-{{ domain }}:
    cmd.run:
        - name: find /etc/opendkim/keys/{{ domain }} -type f ! -name "{{ selector }}.private" -delete -print


opendkim-host-key-{{ domain }}-{{ selector }}:
    file.managed:
        - name: /etc/opendkim/keys/{{ domain }}/{{ selector }}.private
        - contents_pillar: OPENDKIM_KEY_{{ selector }}
        - show_diff: False
        - user: root
        - group: opendkim
        - mode: 640
        - require:
            - file: opendkim-host-key-dir-{{ domain }}
        - watch_in:
            - service: opendkim
{% endfor %}
