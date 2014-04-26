core-packages:
  pkg.installed:
    - order: 1
    - pkgs:
      - curl
      - vim
      - wget


absent-packages:
  pkg.purged:
    - pkgs:
      - whoopsie
