from html.parser import HTMLParser
from requests import get


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


def getArtistsAndAlbums():
    parser = MyParser()
    parser.feed(get("https://pitchfork.com/reviews/best/albums/").text)
    artists_albums = combine(parser.artists, parser.albums)
    parser.close()
    return artists_albums
