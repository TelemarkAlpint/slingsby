from articles.models import Article, ArticleForm, SubPageArticle, \
    SubPageArticleForm
from django.contrib import admin
from general.time import now

class ArticleAdmin(admin.ModelAdmin):
    form = ArticleForm

    def save_model(self, request, obj, form, change):
        instance = form.save(commit=False)
        if not hasattr(instance,'author'):
            instance.author = request.user
        else:
            instance.last_edited_by = request.user
            instance.last_edited = now()
        instance.save()
        return instance

class SubPageArticleAdmin(admin.ModelAdmin):
    form = SubPageArticleForm

    def save_model(self, request, obj, form, change):
        instance = form.save(commit=False)
        if not hasattr(instance,'author'):
            instance.author = request.user
        else:
            instance.last_edited_by = request.user
            instance.last_edited = now()
        instance.save()
        return instance

admin.site.register(Article, ArticleAdmin)
admin.site.register(SubPageArticle, SubPageArticleAdmin)
