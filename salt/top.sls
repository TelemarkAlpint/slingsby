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
    - networking

  'vagrant-fileserver':
    - networking

  'roles:fileserver':
    - match: grain
    - fileserver

  'roles:web':
    - match: grain
    - duplicity
    - old-sites
    - postgres
    - slingsby
    - sshfs
