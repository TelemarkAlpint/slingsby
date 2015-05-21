base:
  '*':
    - iptables
    - ntp
    - pkg
    - sudo
    - swap
    - users

  'ntnuita.no':
    - ssh

  'vagrant':
    - networking

  'vagrant-fileserver':
    - networking

  'roles:fileserver':
    - match: grain
    - mysql.server
    - fileserver

  'roles:web':
    - match: grain
    - old-sites
    - slingsby
    - sshfs
