from .common import EditorialNotes
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .albums import AlbumsRelationship

class ArtistAttributes:
    """
    editorialNotes: The notes about the artist: EditorialNotes
    genreNames: the names of the genres associated with the artist: [str]
    name: The localized name of the artist: string
    url: the url for sharing the artist: string
    """
    def __init__(self, data):
        self.editorialNotes: EditorialNotes = EditorialNotes(data.get('editorialNotes'))
        self.genreNames: List[str] = data.get('genreNames')
        self.name: str = data.get('name')
        self.url: str = data.get('url')

class ArtistRelationships:
    def __init__(self,
                albums: 'AlbumsRelationship'):
        self.albums: AlbumsRelationship = albums
        #self.genres: GeneresRelationship = GeneresRelationship(data.get('genres'))
        #self.musicVideos: MusicVideosRelationship = MusicVideosRelationship(data.get('musicVideos'))
        #self.playlists: PlaylistsRelationship = PlaylistsRelationship(data.get('playlists'))
        #self.station: StationRelationship = StationRelationship(data.get('station'))


class Artist:
    """
    id: The identifier for the artist: string
    href: The relative location for the artist resource: href
    attributes: Attributes for the artist: ArtistsAttributes
    relationships: Relationships for the artist: ArtistsRelationships
    views: Views for the artist: ArtistsViews
    """
    def __init__(self, data, relationships: Optional[ArtistRelationships] = None):
        self.id: str = data.get("id")
        self.href: str = data.get("href")
        self.attributes: Optional[ArtistAttributes] = ArtistAttributes(data.get("attributes")) if data.get("attributes") else None
        self.relationships: Optional[ArtistRelationships] = relationships


class ArtistsRelationship:
    """
    href: The relative location to fetch the relationship directly: string
next: The next page of the relationship: string
    data: The data in the relationship: [Artists]
    """
    def __init__(self, data):
        self.href: str = data.get('href')
        self.next: str = data.get('next')
        self.data: List[Artist] = [Artist(item, None) for item in data.get('data')]