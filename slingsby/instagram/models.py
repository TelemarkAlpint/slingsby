from django.db import models

class InstagramMedia(models.Model):
    media_type = models.CharField('type', max_length=15)
    poster = models.CharField('poster', max_length=40)
    poster_image = models.URLField('posters profilbilde')
    thumbnail_url = models.URLField('link til thumbnail')
    media_url = models.URLField('link til media')
    like_count = models.IntegerField('antall likes')
    caption = models.TextField('tekst')
    created_time = models.DateTimeField('tid opprettet')
    instagram_id = models.CharField('instgram id', max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'instagram media'


    def __unicode__(self):
        return '%s: %s' % (self.poster, self.caption[:80])

    @property
    def comments(self):
        return self._comments.all()


class InstagramComment(models.Model):
    poster = models.CharField('poster', max_length=40)
    poster_image = models.URLField('posters profilbilde')
    created_time = models.DateTimeField('tid opprettet')
    instagram_id = models.CharField('instagram id', max_length=100, unique=True)
    text = models.TextField('tekst')
    media = models.ForeignKey(InstagramMedia, related_name='_comments')

    def __unicode__(self):
        return '%s: %s' % (self.poster, self.text[:80])
