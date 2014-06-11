# Use this module to set up where the different resources are located in the different environments,
# such that dev boxes only use local resources, and prod boxes use RDS f. ex

# pillar states defined later in the pillar/top.sls file will override earlier states, so you can
# set defaults here, and override for environment specific stuff in later states

env:
  db_uri: db-slingsby-rel.crj3xomafakq.eu-west-1.rds.amazonaws.com
