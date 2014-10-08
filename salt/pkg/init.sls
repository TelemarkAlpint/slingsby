core-packages:
  pkg.installed:
    - order: 1
    - pkgs:
      - curl
      - python-software-properties
      - vim
      - wget


absent-packages:
  pkg.purged:
    - pkgs:
      - whoopsie
