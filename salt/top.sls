base:
  '*':
    - ntp
    - pkg
    - sudo
    - swap
    - users

  'ntnuita.no':
    - ssh

  'vagrant':
    - mysql.server
    - networking

  'vagrant-fileserver':
    - networking

  'roles:fileserver':
    - match: grain
    - fileserver

  'roles:web':
    - match: grain
    - old-sites
    - slingsby
    - sshfs
