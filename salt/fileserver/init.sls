# This state is not used in production, only to simulate having
# org.ntnu.no available in a dev environement

include:
  - nginx

fileserver:
  file.directory:
    - name: /srv/fileserver
    - user: root
    - group: fileserver
    - mode: 775
    - require:
      - user: fileserver

  user.present:
    - name: fileserver

  ssh_auth.present:
    - user: fileserver
    - name: ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQD2Rbpo8bSmhf+LH95YqnQ+/8VJRhwYg07wy3AmGIINLfTUnuWOYSy8/mUDEif6kIH8v0+m5UhGzp7hqxaWgcuYyqTJ8yWYQ1pUiw/5KqOPQEW0JWXqzcxCGXc0iWqZmkh6ANHzOfrOX4/JPHr84RAwaUYKsYySQjppeAiZkk3lnd84LhC2vJ/ffPDRkDc+CfHDPMw/sTxMXVBUwfi4fjF4kgkeb6qU/FgNu1WCWFNmp6ChHrLS6N2nWqhKUgpYkuwImvfmYAAGWlZJzMKl/PJhZ0T1YPkqk1sINn91lhUHj0Pt4fd9PHDwW72q3zyx2+jxVJzYQoN/jFctyHW07uxr vagrant@vagrant-ubuntu-trusty-64
    - require:
      - user: fileserver


fileserver-nginx-site:
  file.managed:
    - name: /etc/nginx/sites-enabled/media.ntnuica.local
    - source: salt://fileserver/fileserver-nginx-site
    - require:
      - pkg: nginx
    - watch_in:
      - service: nginx


fileserver-backup-directory:
  file.directory:
    - name: /var/backups/slingsby
    - user: root
    - group: fileserver
    - mode: 775
