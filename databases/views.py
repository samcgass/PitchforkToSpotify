from django.shortcuts import render
from databases.models import AllBestNewMusic, AllHighlyRatedAlbums
from databases.update import getArtistsAndAlbums


def update(request):
    try:
        updateDatabases()
        return render(request, "update.html")
    except:
        return render(request, "error.html")


def updateHighlyRatedDatabases():
    text_albums, status = getArtistsAndAlbums(True, 1)
    for album in text_albums:
        try:
            AllHighlyRatedAlbums.objects.get(album=album[1], artist=album[0])
            return
        except AllHighlyRatedAlbums.DoesNotExist:
            alb = AllHighlyRatedAlbums(album=album[1], artist=album[0])
            alb.save()
    page_num = 2
    while status < 300:
        text_albums, status = getArtistsAndAlbums(True, page_num)
        for album in text_albums:
            try:
                AllHighlyRatedAlbums.objects.get(
                    album=album[1], artist=album[0])
                return
            except AllHighlyRatedAlbums.DoesNotExist:
                alb = AllHighlyRatedAlbums(album=album[1], artist=album[0])
                alb.save()
        page_num += 1


def updateBestNewMusicDatabases():
    text_albums, status = getArtistsAndAlbums(False, 1)
    for album in text_albums:
        try:
            AllBestNewMusic.objects.get(album=album[1], artist=album[0])
            return
        except AllBestNewMusic.DoesNotExist:
            alb = AllBestNewMusic(album=album[1], artist=album[0])
            alb.save()
    page_num = 2
    while status < 300:
        text_albums, status = getArtistsAndAlbums(True, page_num)
        for album in text_albums:
            try:
                AllBestNewMusic.objects.get(album=album[1], artist=album[0])
                return
            except AllBestNewMusic.DoesNotExist:
                alb = AllBestNewMusic(album=album[1], artist=album[0])
                alb.save()
        page_num += 1


def updateDatabases():
    updateBestNewMusicDatabases()
    updateHighlyRatedDatabases()
