# Use this module to set up where the different resources are located in the different environments,
# such that dev boxes only use local resources, and prod boxes use RDS f. ex

{% if grains.id == 'vagrant' %}
env:
  db_uri: localhost
  slingsby:
    bind_url: ntnuita.local
{% else %}
env:
  db_uri: db-slingsby-rel.crj3xomafakq.eu-west-1.rds.amazonaws.com
  slingsby:
    bind_url: ntnuita.no
{% endif %}
