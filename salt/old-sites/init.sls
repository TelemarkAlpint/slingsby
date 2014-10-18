/srv/old-sites/2004:
  file.directory:
    - makedirs: True


site-2004:
  file.managed:
    - name: /usr/local/src/2004.tar.gz
    - source: http://org.ntnu.no/telemark/arkiv/websites/telemark-2004.tar.gz
    - source_hash: http://org.ntnu.no/telemark/arkiv/websites/telemark-2004.tar.gz.sha

  cmd.wait:
    - name: tar xf /usr/local/src/2004.tar.gz -C /srv/old-sites/2004
    - require:
      - file: /srv/old-sites/2004
    - watch:
      - file: site-2004
