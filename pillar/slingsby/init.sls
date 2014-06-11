slingsby:
  db_password: {{ pillar.get('MYSQL_PASSWORD', 'unset')}}
  secret_key: {{ pillar.get('SECRET_KEY', 'unset')}}
