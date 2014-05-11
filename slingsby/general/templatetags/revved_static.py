"""
    Override static file handling so that we can serve revved files, but access them using their
    non-revved filenames.

    Set settings.FILEREVS to point to output from grunt-filerev-assets or similar, where the output
    is a JSON file of the form:

        {
            'css/styles.css': 'css/styles.cafed00d.css'
        }

    Now, load the tag library and continue using the static tag as you had previously:

        {% load revved_static %}

        <link rel="stylesheets" href="{% static 'css/styles.css' %}">

    Would return

        <link rel="stylesheet" href="css/styles.cafed00d.css">

    If a file is not found in filerev mapping, we'll fall back to the normal staticfiles behavior.
"""

from django import template
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.staticfiles.templatetags.staticfiles import StaticFilesNode
import json
from os import path

register = template.Library()

class FileRevNode(StaticFilesNode):

    def load_filerevs(self, filerevs_path):
        if not path.exists(filerevs_path):
            raise template.TemplateSyntaxError("The filerevs specified by settings.FILEREVS ('%s') does not exist." % filerevs_path)
        with open(filerevs_path) as fh:
            self.filerevs = json.load(fh)


    def url(self, context):
        path = self.path.resolve(context)
        revved_path = self.filerevs.get(path)
        if revved_path is not None:
            return staticfiles_storage.url(revved_path)
        else:
            return super(FileRevNode, self).url(context)


@register.tag
def static(parser, token):
    static_node = FileRevNode.handle_token(parser, token)
    static_node.load_filerevs(settings.FILEREVS)
    return static_node
