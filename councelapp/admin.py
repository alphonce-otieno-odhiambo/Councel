from django.contrib import admin
from .models import * 

# Register your models here.
admin.site.register(ClientProfile)
admin.site.register(Group)
admin.site.register(Counsellor)
admin.site.register(CounselorProfile)
admin.site.register(Conversation)
admin.site.register(Message)
admin.site.register(Counselling)
