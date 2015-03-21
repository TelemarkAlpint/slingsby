slingsby:
  # Not necessary to keep it in quotes, but we do so to keep it as valid yaml both before and
  # after jinja processing, so that fabric can extract the fileserver-related options without
  # rendering the file with jinja
  db_password: "{{ pillar.get('DB_PASSWORD', 'unset') }}"
  secret_key: "{{ pillar.get('SECRET_KEY', 'unset') }}"
  fileserver: tarjeikl@login.stud.ntnu.no
  fileserver_media_root: /home/groupswww/telemark/media/
  backup_directory: '/home/groups/telemark/backup'
