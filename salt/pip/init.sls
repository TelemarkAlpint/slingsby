# Install latest pip, first from repo, and then update from PyPI
pip:
  pkg.installed:
    - name: python-pip

  pip.installed:
    - require:
      - pkg: pip
    - upgrade: True
