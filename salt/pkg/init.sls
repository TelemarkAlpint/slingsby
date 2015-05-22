core-packages:
  pkg.installed:
    - order: 1
    - pkgs:
      - at
      - curl
      - python-software-properties
      - vim
      - wget


absent-packages:
  pkg.purged:
    - pkgs:
      - whoopsie
