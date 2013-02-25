from BeautifulSoup import BeautifulSoup
from contextlib import closing
from django.http import HttpResponse
from google.appengine.api.urlfetch import fetch
from urllib2 import urlopen
from users.models import NameLookup, UserProfile
import logging

def sync_profile_images(request):
    def has_image(user_profile):
        img_url = 'http://www.ntnui.no/%d.large.user.profile.jpg' % user_profile.ntnui_id
        try:
            with closing(urlopen(img_url)) as webpage:
                logging.info('Found user img!')
                return True
        except:
            return False

    logging.info('Syncing profile images')
    for user in UserProfile.objects.exclude(ntnui_id=None):
        logging.info("Found user: " + str(user))
        user.has_image = has_image(user)
        user.save()
    return HttpResponse()

def sync_users(request):
    logging.info('Starting sync.')
    old_names = get_old_names_as_set()
    logging.info('Found %d old names.' % len(old_names))
    current_list = get_site_names_as_set()
    logging.info('Found %d names on the site.' % len(current_list))
    new_names = current_list - old_names
    for name in new_names:
        lookup = name.create_NameLookup()
        lookup.save()
    logging.info('%d names added.' % len(new_names))
    return HttpResponse()

def get_old_names_as_set():
    all_names = NameLookup.objects.all()
    temps = []
    for name in all_names:
        if name.name:
            temp = TempName(name.name, name.email)
            temps.append(temp)
        else:
            logging.info('Deleting old name' + name.email)
            name.delete()
    return set(temps)

def get_site_names_as_set():
    html = get_raw_html('http://www.ntnui.no/telemark/printMembers')
    soup = BeautifulSoup(html)
    table = soup.findAll('table', limit=3)[-1]
    rows = table.findAll('tr')
    new_names = set()
    for row in rows:
        cols = row.findAll('td')[:2]
        person_data = []
        if cols:
            for col in cols:
                data = ''.join(col.find(text=True))
                person_data.append(data)
            name = TempName(*person_data)
            new_names.add(name)
    return new_names

def get_raw_html(url):
    page = fetch(url)
    return page.content

class TempName():
    name = None
    email = None

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def create_NameLookup(self):
        name = NameLookup(name=self.name, email=self.email)
        return name

    def __unicode__(self):
        return self.name

    def __key__(self):
        return (self.name, self.email)

    def __eq__(self, other):
        return self.__key__() == other.__key__()

    def __hash__(self):
        return hash(self.__key__())
