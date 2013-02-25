from django.contrib import admin
from musikk.models import Song, Vote, AdminVoteForm, AdminSongForm

class SongAdmin(admin.ModelAdmin):
    form = AdminSongForm
    readonly_fields = ('votes', 'date_added', 'popularity')

class VoteAdmin(admin.ModelAdmin):
    form = AdminVoteForm
    readonly_fields = ('date_added', 'song', 'user', 'counted')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        if obj is not None:
            if obj.counted:
                return False
        return True

admin.site.register(Song, SongAdmin)
admin.site.register(Vote, VoteAdmin)