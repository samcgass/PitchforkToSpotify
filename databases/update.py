from html.parser import HTMLParser
from requests import get
from databases.models import AllHighlyRatedAlbums, AllBestNewMusic


class MyParser(HTMLParser):
    nextDataIsAlbum = False
    nextDataIsArtist = False
    albums = []
    artists = []

    def handle_starttag(self, tag, attrs):
        if ("class", "review__title-album") in attrs:
            self.nextDataIsAlbum = True
        elif ("class", "artist-list review__title-artist") in attrs:
            self.nextDataIsArtist = True

    def handle_data(self, data):
        if self.nextDataIsAlbum:
            self.albums.append(data)
            self.nextDataIsAlbum = False
        if self.nextDataIsArtist:
            self.artists.append(data)
            self.nextDataIsArtist = False

    def error(self, message):
        pass


def combine(list1, list2):
    one_list = []
    for pair in zip(list1, list2):
        one_list.append(pair)
    return one_list


def getArtistsAndAlbums(all_highly_rated, page):
    parser = MyParser()
    if all_highly_rated:
        res = get(
            "https://pitchfork.com/best/high-scoring-albums/?page=" + str(page))
    else:
        res = get("https://pitchfork.com/reviews/best/albums/?page=" + str(page))
    parser.feed(res.text)
    artists_albums = combine(parser.artists, parser.albums)
    parser.close()
    return artists_albums, res.status_code


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
