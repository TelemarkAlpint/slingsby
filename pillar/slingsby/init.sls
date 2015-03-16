slingsby:
  db_password: {{ pillar.get('DB_PASSWORD', 'unset')}}
  secret_key: {{ pillar.get('SECRET_KEY', 'unset')}}
  fileserver: tarjeikl@login.stud.ntnu.no
  fileserver_media_root: /home/groupswww/telemark/media/
  backup_directory: '/home/groups/telemark/backup'
