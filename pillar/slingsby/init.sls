slingsby:
  db_password: {{ pillar.get('MYSQL_PASSWORD', 'unset')}}
  secret_key: {{ pillar.get('SECRET_KEY', 'unset')}}
  fileserver: tarjeikl@login.stud.ntnu.no
  fileserver_media_root: /home/groupswww/telemark/media/
