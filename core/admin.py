# filepath: [admin.py](http://_vscodecontentref_/1)
from django.contrib import admin
from .models import User, Profile, Project, Proposal, Message, Review

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Project)
admin.site.register(Proposal)
admin.site.register(Message)
admin.site.register(Review)