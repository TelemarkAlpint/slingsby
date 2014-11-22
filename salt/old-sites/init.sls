{% set old_sites = pillar.get('old_sites', []) %}

{% for site in old_sites %}

/srv/old-sites/{{ site }}:
  file.directory:
    - makedirs: True


site-{{ site }}:
  file.managed:
    - name: /usr/local/src/{{ site }}.tar.gz
    - source: http://org.ntnu.no/telemark/arkiv/websites/telemark-{{ site }}.tar.gz
    - source_hash: http://org.ntnu.no/telemark/arkiv/websites/telemark-{{ site }}.tar.gz.sha

  cmd.wait:
    - name: tar xf /usr/local/src/{{ site }}.tar.gz -C /srv/old-sites/{{ site }}
    - require:
      - file: /srv/old-sites/{{ site }}
    - watch:
      - file: site-{{ site }}

{% endfor %}
