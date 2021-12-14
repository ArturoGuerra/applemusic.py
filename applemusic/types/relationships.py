




class MusicVideosRelationship:
    """
    href: str The relative location to fetch the relationship directly
    next: str The next page of the relationship
    data: [MusicVideos]
    """
    def __init__(self, data):
        self.href: str = data.get('href')
        self.next: str = data.get('next')
        self.data: [MusicVideo] = [MusicVideo(item) for item in data.get('data')]


class LibraryAlbumsRelationship:
    """
    href: The relative location to fetch the relationship directly: string
    next: The next page of the relationship: string
    data: The data in the relationship: [Library]
    """
    def __init__(self, data):
        self.href: str = data.get('href')
        self.next: str = data.get('next')
        self.data: [Library] = [Library(item) for item in data.get('data')]



class LibraryArtistsRelationship:
    """
    href: The relative location to fetch the relationship directly: string
    next: The next page of the relationship: string
    data: The data in the relationship: [Artists]
    """
    def __init__(self, data):
        self.href: str = data.get('href')
        self.next: str = data.get('next')
        self.data: [Artist] = [Artist(item) for item in data.get('data')]


class LibrarySongsRelationship:
    """
    href: The relative location to fetch the relationship directly: string
    next: The next page of the relationship: string
    data: The data in the relationship: [Tracks]
    """
    def __init__(self, data):
        self.href: str = data.get('href')
        self.next: str = data.get('next')
        self.data: [Song] = [Song(item) for item in data.get('data')]

class LibraryMusicVideosRelationship:
    """
    href: str The relative location to fetch the relationship directly
    next: str The next page of the relationship
    data: [MusicVideos]
    """
    def __init__(self, data):
        self.href: str = data.get('href')
        self.next: str = data.get('next')
        self.data: [MusicVideo] = [MusicVideo(item) for item in data.get('data')]