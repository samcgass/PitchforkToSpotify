from django.shortcuts import render
from databases.models import AllBestNewMusic, AllHighlyRatedAlbums
from databases.update import getArtistsAndAlbums
from django.utils.dateparse import parse_datetime


def update(request):
    updateDatabases()
    return render(request, "update.html")


def updateHighlyRatedDatabases():
    text_albums, status = getArtistsAndAlbums(True, 1)
    for album in text_albums:
        try:
            AllHighlyRatedAlbums.objects.get(
                album=album[1], artist=album[0])
            return
        except AllHighlyRatedAlbums.DoesNotExist:
            alb = AllHighlyRatedAlbums(
                album=album[1], artist=album[0], date=parse_datetime(album[2]))
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
                alb = AllHighlyRatedAlbums(
                    album=album[1], artist=album[0], date=parse_datetime(album[2]))
                alb.save()
        page_num += 1


def updateBestNewMusicDatabases():
    text_albums, status = getArtistsAndAlbums(False, 1)
    for album in text_albums:
        try:
            AllBestNewMusic.objects.get(
                album=album[1], artist=album[0])
            return
        except AllBestNewMusic.DoesNotExist:
            alb = AllBestNewMusic(
                album=album[1], artist=album[0], date=parse_datetime(album[2]))
            alb.save()
    page_num = 2
    while status < 300:
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
