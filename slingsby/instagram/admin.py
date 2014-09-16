from .models import InstagramMedia, InstagramComment
from django.contrib import admin

class SongAdmin(admin.ModelAdmin):
#    form = AdminSongForm
    readonly_fields = ('votes', 'date_added', 'popularity')

class VoteAdmin(admin.ModelAdmin):
    #form = AdminVoteForm
    readonly_fields = ('date_added', 'song', 'user', 'counted')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        if obj is not None:
            if obj.counted:
                return False
        return True

admin.site.register(InstagramMedia)
admin.site.register(InstagramComment)
