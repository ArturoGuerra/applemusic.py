from typing import Optional, TYPE_CHECKING
from .common import Preview, Artwork, PlayParameters
if TYPE_CHECKING:
    from .albums import AlbumsRelationship
    from .artists import ArtistsRelationship

class SongAttributes:
    """
    albumName: str
    artistName: str
    artwork: Artwork
    attribution: str
    composerName: str
    contentRating: str
    discNumber: int
    durationInMillis: int
    editorialNotes: EditorialNotes
    genreNames: [str]
    hasLyrics: bool
    isrc: str
    movementCount: int
    movementName: str
    movementNumber: int
    name: str
    playParams: PlayParameters
    previews: [Preview]
    releaseDate: str
    trackNumber: int
    url: str
    """
    def __init__(self, data):
        self.albumName: str = data.get('albumName')
        self.artistName: str = data.get('artistName')
        self.artwork: Artwork = Artwork(data.get('artwork'))    
        self.attribution: Optional[str] = data.get('attribution', None)
        self.composerName: Optional[str] = data.get('composerName', None)
        self.contentRating: Optional[str] = data.get('contentRating', None)
        self.discNumber: Optional[int] = data.get('discNumber', None)
        self.durationInMillis: int = data.get('durationInMillis')
        self.editorialNotes: Optional[EditorialNotes] = EditorialNotes(data.get('editorialNotes')) if data.get('editorialNotes') else None
        self.genreNames: [str] = data.get('genreNames')
        self.hasLyrics: bool = data.get('hasLyrics')
        self.isrc: Optional[str] = data.get('isrc', None)
        self.movementCount: Optional[int] = data.get('movementCount', None)
        self.movementName: Optional[str] = data.get('movementName', None)
        self.movementNumber: Optional[int] = data.get('movementNumber', None)
        self.name: str = data.get('name')
        self.playParams: Optional[PlayParameters] = PlayParameters(data.get('playParams')) if data.get('playParams') else None
        self.previews: [Preview] =[Preview(item) for item in data.get('previews')]
        self.releaseDate: Optional[str] = data.get('releaseDate', None)
        self.trackNumber: Optional[int] = data.get('trackNumber', None)
        self.url: str = data.get('url')

class SongRelationships:
    """
    albums: AlbumsRelationship
    artists: ArtistsRelationship
    genres: GenresRelationship
    station: StationRelationship
    composers: ComposersRelationship
    library: LibrarySongsRelationship
    music-videos: MusicVideosRelationship
    """
    def __init__(self,
                albums: 'AlbumsRelationship',
                artists: 'ArtistsRelationship'):
        self.albums: AlbumsRelationship = albums
        self.artists: ArtistsRelationship = artists
        #self.genres: GenresRelationship = GenresRelationship(data.get('genres'))
        #self.station: StationRelationship = StationRelationship(data.get('station'))
        #self.composers: ComposersRelationship = ComposersRelationship(data.get('composers'))
        #self.library: LibrarySongsRelationship = LibrarySongsRelationship(data.get('library'))
        #self.musicVideos: MusicVideosRelationship = MusicVideosRelationship(data.get('musicVideos'))

class Song:
    """
    id: str The indentifier for the song
    href: str The relative location for the song resource
    attributes: SongAttributes
    relationships: SongRelationships
    """
    def __init__(self, data, relationships: Optional[SongRelationships] = None):
        self.id: str = data.get('id')
        self.href: str = data.get('href')
        self.attributes: Optional[SongAttributes] = SongAttributes(data.get('attributes')) if data.get('attributes') else None
        self.relationships: Optional[SongRelationships] = relationships

class SongsRelationship:
    """
    href: The relative location to fetch the relationship directly: string
    next: The next page of the relationship: string
    data: The data in the relationship: [Tracks]
    """
    def __init__(self, data):
        self.href: str = data.get('href')
        self.next: str = data.get('next')
        self.data: [Song] = [Song(item, None) for item in data.get('data')]