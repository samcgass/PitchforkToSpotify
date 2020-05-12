from django.contrib import admin
from best_new_music.models import best_new_music


class BestNewMusicAdmin(admin.ModelAdmin):
    pass


admin.site.register(best_new_music, BestNewMusicAdmin)
