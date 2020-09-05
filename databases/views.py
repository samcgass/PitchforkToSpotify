from django.shortcuts import render
from django.utils.dateparse import parse_datetime
from databases.models import AllBestNewMusic, AllHighlyRatedAlbums
from databases.update import getArtistsAndAlbums


def update(request):
    try:
        updateDatabases()
        return render(request, "update.html")
    except:  # pylint: disable=bare-except
        return render(request, "error.html")


def updateHighlyRatedDatabases():
    page_num = 1
    status = 200
    while status < 300:
        text_albums = []
        text_albums, status = getArtistsAndAlbums(True, page_num)
        for album in text_albums:
            try:
                AllHighlyRatedAlbums.objects.get(
                    album=album[1], artist=album[0])
                return
            except AllHighlyRatedAlbums.DoesNotExist:
                alb = AllHighlyRatedAlbums(
                    album=album[1], artist=album[0], date=parse_datetime(album[2]))
                alb.save()
        page_num += 1


def updateBestNewMusicDatabases():
    page_num = 1
    status = 200
    while status < 300:
        text_albums = []
        text_albums, status = getArtistsAndAlbums(False, page_num)
        for album in text_albums:
            try:
                AllBestNewMusic.objects.get(
                    album=album[1], artist=album[0])
                return
            except AllBestNewMusic.DoesNotExist:
                alb = AllBestNewMusic(
                    album=album[1], artist=album[0], date=parse_datetime(album[2]))
                alb.save()
        page_num += 1


def updateDatabases():
    updateBestNewMusicDatabases()
    updateHighlyRatedDatabases()
