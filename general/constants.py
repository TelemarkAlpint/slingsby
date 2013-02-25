
# Hvis denne endres mA ogsA ADMIN_MEDIA_PREFIX i settings.py endres.
STATIC_DIR = 'http://org.ntnu.no/telemark/static/'

GRAPHICS_DIR = 'http://org.ntnu.no/telemark/static/gfx/'

LOGIN_URL = 'http://ntnui.no/authapi/telemark'

LOGOUT_URL = 'http://ntnui.no/Logout.xhtml'

LOGIN_REDIRECT = 'http://ntnui.no/telemark'

MEDIA_DIR = 'http://org.ntnu.no/telemark/media/'

MUSIC_DIR = MEDIA_DIR + 'songs/'

# Why the funny ending? See http://docs.python.org/2/faq/design.html#why-can-t-raw-strings-r-strings-end-with-a-backslash
LOCAL_MUSIC_DIR = r'\\webedit.ntnu.no\groupswww\telemark\media\songs' '\\'

BASE_URL = 'http://telemarkalpint.appspot.com'

JSON_ARCHIVE_PATH = 'http://org.ntnu.no/telemark/arkiv/arrangement/archive.json'

DEFAULT_TITLE = 'NTNUI Telemark/Alpint'

JOIN_URL = 'http://ntnui.no/telemark/Join.xhtml'

LEAVE_URL = 'http://ntnui.no/telemark/Leave.xhtml'

EDIT_PROFILE_IMAGE = 'http://www.ntnui.no/Profile/Edit/Image.xhtml'

ARCHIVE_BASE_PATH = 'http://org.ntnu.no/telemark/arkiv/arrangement/'