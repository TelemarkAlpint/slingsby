# coding: utf-8

from django.utils.safestring import SafeUnicode

_all_feedbacks = {}

class Feedback():
    urlcode = ''
    feedback = ''
    
    def __init__(self, urlcode, feedback):
        feedback = SafeUnicode(feedback)
        _all_feedbacks[urlcode] = feedback
        self.urlcode = urlcode
        self.feedback = feedback
        
    def format_string(self, *args):
        new_code = self.urlcode + str(hash(str(args)))
        _all_feedbacks[new_code] = self.feedback % args
        return new_code
    
    def __unicode__(self):
        return self.urlcode
    
    def __str__(self):
        return self.urlcode
    
def get_feedback(urlcode):
    return _all_feedbacks.get(urlcode)
    

MUSIC_READY = Feedback('ready', u'Ny sang lastet opp i databasen, tusen takk!')

QUOTE_THANKS = Feedback('qthanks', u'Takk for forslaget, teknisk ansvarlig vil se på sitatet ASAP!')

BOBBY = Feedback('bobby', u'<img src="http://imgs.xkcd.com/comics/exploits_of_a_mom.png" alt="Bobby Tables">')

FU = Feedback('fu', u'Stikk av!')

SONG_THANKS = Feedback('thanks', u'Takk for forslaget! Teknisk ansvarlig vil laste opp sangen asap!')

SONG_DELETED = Feedback('deleted', u'%s slettet!')

SONG_VOTED_UP = Feedback('songup', u'Du stemte opp %s!')

SONG_VOTED_DOWN = Feedback('songdown', u'Du stemte ned %s!')

SONG_READY = Feedback('songready', u'%s er nå klar til å stemmes på!')

EVENT_SIGN_OFF = Feedback('eventoff', u'Du meldte deg av %s.')

EVENT_SIGN_ON = Feedback('eventon', u'Du meldte deg på %s.')

NAME_COMP = Feedback('name', u'Du fylte inn fullt navn, tusen takk!')
