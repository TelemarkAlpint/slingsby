python-pip:
  pkg.installed

# Make sure pip is updated
pip:
  pip.installed:
    - require:
      - pkg: python-pip
    - upgrade: True
