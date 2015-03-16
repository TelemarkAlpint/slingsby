{% set slingsby = pillar.get('slingsby') %}

root-ssh-dir:
  file.directory:
    - name: /root/.ssh
    - user: root
    - group: root
    - mode: 700


sshfs-ssh-config:
  file.managed:
    - name: /root/.ssh/config
    - source: salt://sshfs/ssh_config
    - require:
      - file: root-ssh-dir

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

  # Add a cron job to re-mount in case the mount is lost and not caught by the 'reconnect' option
  cron.present:
    - name: mount -a
    - identifier: sshfs-remount
    - minute: random
