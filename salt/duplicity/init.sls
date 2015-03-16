{% set slingsby = pillar.get('slingsby') %}
{% set duplicity = pillar.get('duplicity', {}) %}
{% set version_identifier = duplicity.get('version_identifier', '0.7.01 sha1=d10099ddc88a860c4f0f95bdc8614f14b29e23d9') %}
{% set version, source_hash = version_identifier.split() %}

duplicity-deps:
    pkg.installed:
        - pkgs:
            - python-paramiko
            - python-dev
            - python-pip
            - librsync-dev

    pip.installed:
        - name: lockfile
        - require:
            - pkg: duplicity-deps


duplicity-source:
    file.managed:
        - name: /usr/local/src/duplicity-{{ version }}.tar.gz
        - source: https://code.launchpad.net/duplicity/0.7-series/{{ version }}/+download/duplicity-{{ version }}.tar.gz
        - source_hash: {{ source_hash }}

    cmd.wait:
        - name: tar xf duplicity-{{ version }}.tar.gz
        - cwd: /usr/local/src
        - require:
            - pip: duplicity-deps
        - watch:
            - file: duplicity-source


duplicity:
    cmd.wait:
        - name: python setup.py install
        - cwd: /usr/local/src/duplicity-{{ version }}
        - watch:
            - cmd: duplicity-source


duplicity-passprase:
    cron.env_present:
        - name: PASSPHRASE
        - value: {{ pillar.get('DUPLICITY_PASSPHRASE') }}


duplicity-backup-web:
    cron.present:
        # If any of these settings are changed, also change them in the fabfile.py backup tasks
        - name: duplicity
                --verbosity warning
                --no-print-statistics
                --gpg-options="--cipher-algo=AES256 --digest-algo=SHA512 --s2k-digest-algo=SHA512"
                --asynchronous-upload
                {% for dir in ('etc', 'home', 'opt', 'srv', 'var') %}
                --include /{{ dir }}
                {% endfor %}
                --exclude '**'
                /
                sftp://{{ slingsby.fileserver }}/{{ slingsby.backup_directory }}/
        - identifier: duplicity-backup-web
        - minute: random
        - hour: '*/6'
