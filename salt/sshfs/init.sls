{% set slingsby = pillar.get('slingsby') %}

sshfs-ssh-config:
  file.managed:
    - name: /root/.ssh/config
    - source: salt://sshfs/ssh_config

sshfs:
  pkg:
    - installed

  file.managed:
    - name: /srv/ntnuita.no/fileserver_key.pem
    - contents_pillar: FILESERVER_KEY
    - user: root
    - group: root
    - mode: 600
    - show_diff: False

  mount.mounted:
    - name: /srv/ntnuita.no/media/external
    - device: "{{ slingsby.fileserver }}:{{ slingsby.fileserver_media_root }}"
    - fstype: fuse.sshfs
    - mkmnt: True
    - opts:
      - _netdev
      - allow_other
      - reconnect
      - uid=uwsgi
      - gid=uwsgi
    - require:
      - pkg: sshfs
      - file: sshfs
      - file: sshfs-ssh-config
