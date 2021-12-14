from .common import Artwork, EditorialNotes, PlayParameters
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .artists import ArtistsRelationship
    from .generes import GenresRelationship
    from .songs import SongsRelationship
    from .recordlabels import RecordLabelsRelationship


class AlbumAttributes:
    """
    artistName: The name of the artist who created the album.: string
    artistUrl: The URL of the artist who created the album.: string
    artwork: The Artwork of the album: Artwork
    contentRating: The content rating of the album. Can be one of the following: explicit, clean: string
    copyright: The copyright message for the album.: string
    editorialNotes: The editorial notes for the album. The notes can contain HTML, so clients should be able to render them in the context of the user's locale: EditorialNotes
    genreNames: The genres of the album. For example: "Prog Rock", "Post-grunge": [string]
    isCompilation: Whether the album is a compilation.: boolean
    isComplete: Whether the album is complete. A complete album is one where all media is available: boolean
    isMasteredForItunes: Whether the album is mastered for iTunes: boolean
    isSingle: Whether the album is a single. A single album is one where only a single track is available: boolean
    name: The name of the album.: string
    playParams: The parameters to use to play back the track. : PlayParameters
    recordLabel: The record label for the album.: string
    releaseDate: The release date of the album. This is an ISO 8601 date: string
    trackCount: The number of tracks on the album.: integer
    upc: The UPC code for the album.: string
    url: The URL of the album.: string
    """
    def __init__(self, data):
        self.artistName: str = data.get('artistName')
        self.artistUrl: str = data.get('artistUrl')
        self.artwork: Artwork = Artwork(data.get('artwork'))
        self.contentRating: str = data.get('contentRating')
        self.copyright: str = data.get('copyright')
        self.editorialNotes: EditorialNotes = EditorialNotes(data.get('editorialNotes'))
        self.genreNames: list = data.get('genreNames')
        self.isCompilation: bool = data.get('isCompilation')
        self.isComplete: bool = data.get('isComplete')
        self.isMasteredForItunes: bool = data.get('isMasteredForItunes')
        self.isSingle: bool = data.get('isSingle')
        self.name: str = data.get('name')
        self.playParams: PlayParameters = PlayParameters(data.get('playParams'))
        self.recordLabel: str = data.get('recordLabel')
        self.releaseDate: str = data.get('releaseDate')
        self.trackCount: int = data.get('trackCount')
        self.upc: str = data.get('upc')
        self.url: str = data.get('url')

        
class AlbumRelationships:
    def __init__(self,
            artists: Optional['ArtistsRelationship'] = None,
            genres: Optional['GenresRelationship'] = None,
            library: Optional['LibraryAlbumsRelationship'] = None,
            tracks: Optional['SongsRelationship'] = None,
            recordLabels: Optional['RecordLabelsRelationship'] = None):
        self.artists: Optional[ArtistsRelationship] = artists
        self.genres: Optional[GeneresRelationship] = genres
        self.tracks: Optional[SongsRelationship] = tracks
        self.library: Optional[LibraryAlbumsRelationship] = library
        self.recordLabels: Optional[RecordLabelsRelationship] = recordLabels

class Album:
    """
    id: Album identifier: string
    type: This value is always "albums": string
    href: The relative lication of the album resoruce: string
    attributes: The attributes of the album: AlbumsAttributes
    relationships: The relationships of the album: AlbumsRelationships
    views: The views of the album: AlbumsViews
    """
    def __init__(self, data, relationships: AlbumRelationships = None):
        self.id: str = data.get("id")
        self.href: str = data.get("href")
        self.attributes: Optional[AlbumAttributes] = AlbumAttributes(data.get("attributes")) if data.get("attributes") else None
        self.relationships: AlbumRelationships = relationships

class AlbumsRelationship:
    """
    href: The relative location to fetch the relationship directly: string
    next: The next page of the relationship: string
    data: The data in the relationship: [Genres]
    """
    def __init__(self, data):
        self.href: str = data.get('href')
        self.next: str = data.get('next')
        self.data: [Album] = [Album(item) for item in data.get('data')]