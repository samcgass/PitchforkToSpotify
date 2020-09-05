from django.contrib import admin
from databases.models import AllBestNewMusic, AllHighlyRatedAlbums


class AllHighlyRatedAlbumsAdmin(admin.ModelAdmin):
    pass


class AllBestNewMusicAdmin(admin.ModelAdmin):
    pass


admin.site.register(AllHighlyRatedAlbums, AllHighlyRatedAlbumsAdmin)
admin.site.register(AllBestNewMusic, AllBestNewMusicAdmin)
