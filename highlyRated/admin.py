from django.contrib import admin
from highlyRated.models import HighlyRatedAlbums


class HighlyRatedAlbumsAdmin(admin.ModelAdmin):
    pass


admin.site.register(HighlyRatedAlbums, HighlyRatedAlbumsAdmin)
