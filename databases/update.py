from html.parser import HTMLParser
from requests import get


class MyParser(HTMLParser):
    nextDataIsAlbum = False
    nextDataIsArtist = False
    albums = []
    artists = []
    dates = []

    def handle_starttag(self, tag, attrs):
        if ("class", "review__title-album") in attrs:
            self.nextDataIsAlbum = True
        elif ("class", "artist-list review__title-artist") in attrs:
            self.nextDataIsArtist = True
        elif ("class", "pub-date") in attrs:
            for attr in attrs:
                if attr[0] == "datetime":
                    self.dates.append(attr[1])
                    break

    def handle_data(self, data):
        if self.nextDataIsAlbum:
            self.albums.append(data)
            self.nextDataIsAlbum = False
        if self.nextDataIsArtist:
            self.artists.append(data)
            self.nextDataIsArtist = False

    def error(self, message):
        pass

    def clear(self):
        self.albums = []
        self.artists = []
        self.dates = []


def combine(list1, list2, list3):
    one_list = []
    for pair in zip(list1, list2, list3):
        one_list.append(pair)
    return one_list


def getArtistsAndAlbums(all_highly_rated, page):
    parser = MyParser()
    parser.clear()
    if all_highly_rated:
        res = get(
            "https://pitchfork.com/best/high-scoring-albums/?page=" + str(page))
    else:
        res = get("https://pitchfork.com/reviews/best/albums/?page=" + str(page))
    parser.feed(res.text)
    artists_albums = combine(parser.artists, parser.albums, parser.dates)
    parser.close()
    return artists_albums, res.status_code
