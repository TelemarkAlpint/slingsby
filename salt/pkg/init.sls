absent_packages:
  pkg.purged:
    - pkgs:
{% for pkg in pillar.get('absent_pkgs', []) %}
      - {{ pkg }}
{% endfor %}
