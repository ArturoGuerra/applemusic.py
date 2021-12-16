from requests import Request, Session
from typing import Dict, Optional, List
from .types import Album, AlbumRelationships, ArtistsRelationship, SongsRelationship
from .errors import APIError
from .utils import auth_check

DEFAULT_STOREFRONT = "us"



"""
Base client that interact with the REST api provided by Apple Inc. for their Apple Music service.
"""
class Client:
    API_BASE: str = "https://api.music.apple.com/v1"
    
    # Apple Music HTTP API Paths
    def __init__(self, token, timeout=10, usertoken=None):
        self.session = Session()
        self.timeout = timeout
        self.usertoken = usertoken
        self.token = token
    
    # Authenticated request to apple's music API
    def _request(self, uri: str, method: str = "GET", data = None, query: Optional[dict]=None):
        url = f"{self.API_BASE}{uri}"
        headers = { "Authorization": f"Bearer {self.token}" }

        if self.usertoken != None:
            headers["Music-User-Token"] = self.usertoken

        print(f"{method}: {url} Headers:{headers} Data:{data} Query:{query}")

        req = Request(method, url, data=data, params=query, headers=headers)
        prepped = self.session.prepare_request(req)
        print(prepped.url)

        resp = self.session.send(prepped, timeout=self.timeout)
        return resp

    # Wrapper for creating an album object
    def _create_album(sellf, data) -> Album:
        rawrelationships = data.get("relationships")

        if rawrelationships:
            artists = ArtistsRelationship(rawrelationships.get("artists"))
            tracks = SongsRelationship(rawrelationships.get("tracks"))
            relationships = AlbumRelationships(artists=artists, tracks=tracks)
        else:
            relationship = None

        album = Album(data=data, relationships=relationships)
        return album

    # Wrapper for creating an artist object
    def _create_artist(self, data) -> Artist:
        pass
    
    # Wrapper for creating a song object
    def _create_song(self, data) -> Song:
        pass
    
    # Wrapper for creating a music video object
    def _create_music_video(self, data) -> MusicVideo:
        pass

    # Wrapper for creating a playlist object
    def _create_playlist(self, data) -> Playlist:
        pass

    # Wrapper for creating a station object
    def _create_station(self, data) -> Station:
        pass
    
    # Wrapper for creating a station genre object
    def _create_station_genre(self, data) -> StationGenre:
        pass
    
    # Wrapper for creating a genre object
    def _create_genre(self, data) -> Genre:
        pass

    # Wrapper for creating a chart object
    def _create_chart(self, data) -> Chart:
        pass

    # Wrapper for creating an activity object
    def _create_activity(self, data) -> Activity:
        pass
    
    # Wrapper for creating a curator object
    def _create_curator(self, data) -> Curator:
        pass

    # Wrapper for creating an apple curator object
    def _create_apple_curator(self, data) -> AppleCurator:
        pass 

    # Wrapper for creating a record label object
    def _create_record_label(self, data) -> RecordLabel:
        pass

    # Wrapper for creating s recommendation object
    def _create_recommendation(self, data) -> Recommendation:
        pass

    # Gets a single api resource by its id
    def _get_catalog_resource(self, resource: str, storefront: str, id: str, query: Dict, relationship: str=None, view: str=None) -> Dict:
        url = f"/catalog/{storefront}/{resource}/{id}"
        if relationship != None:
            url += f"/{relationship}"
        elif view != None:
            url += f"/{view}"
        resp = self._request(url, query=query)
        if resp.status_code != 200:
            raise APIError(resp.status_code, resp.text)
        
        return resp.json()["data"][0]

    # Gets multiple api resources by their ids    
    def _get_catalog_resources(self, resource: str, storefront: str, query: Dict):
        url = f"/catalog/{storefront}/{resource}"
        resp = self._request(url, query=query)
        if resp.status_code != 200:
            raise APIError(resp.status_code, resp.text)
        
        return resp.json()["data"]

    # Fetches a single resource by id from the users library
    def _get_library_resource(self, resource: str, id: str, query: Dict, relationship: str=None, view: str=None):
        url = f"/me/library/{resource}/{id}"
        resp = self._request(url, query=query)
        if resp.status_code != 200:
            raise APIError(resp.status_code, resp.text)
        return resp.json()["data"][0]
    
    # Fetches multiple resources from the users library
    def _get_library_resources(self, resource: str, query):
        url = f"/me/library/{resource}"
        resp = self._request(url, query=query)
        if resp.status_code != 200:
            raise APIError(resp.status_code, resp.text)
        return resp.json()["data"]



    # Fetches an album by its id
    def album(self, id, storefront=DEFAULT_STOREFRONT, l="", include=None, views=None, extend=None) -> Optional[Album]:
        resource = self._get_catalog_resource("albums", storefront, id, {"l": l, "include": include, "views": views, "extend": extend})
        return self._create_album(resource)

    # Fetch multiple albums by their ids
    def albums(self, ids: List[str], storefront: str=DEFAULT_STOREFRONT, include: List[str] = None, l: str=None, extend: List[str] = None) -> List[Album]:
        resources = self._get_catalog_resources("albums", storefront, {"ids": ids, "include": include, "l": l, "extend": extend})
        return [self._create_album(album) for album in resources]

#    # Fetch an album relationship by album id and relationship type
#    def album_relationship(self, id: str, relationship: str, storefront: str=DEFAULT_STOREFRONT, l: str="", include: List[str]=None, limit: int:None, extend: List[str]=None) -> Optional[AlbumRelationship]:
#        resource = self._get_catalog_resource("albums", storefront, id, {"l": l, "include": include, "limit": limit, "extend": extend}, relationship=relationship)
#        return self._create_album_relationship(resource)
#
#    # Fetch album's relationship view by album id and name of resource to view
#    def album_relationship_view(self, id: str, view: str, storefront: str=DEFAULT_STOREFRONT, extend: List[str]=None, include: List[str]=None, l: str=None, limit: int=None, qwith: List[str]: None) -> Optional[AlbumRelationshipView]:
#        resource = self._get_catalog_resource("albums", storefront, id, {"l": l, "include": include, "limit": limit, "extend": extend, "qwith": qwith}, view=view)
#        return self._create_album_relationship_view(resource)

    # Fetch an album from the users libray
    @auth_check
    def library_album(self, id: str, l: str=None, include: List[str]=None, extend: List[str]=None) -> Optional[LibraryAlbum]:
        resource = self._get_library_resource("albums", id, {"l": l, "include": include, "extend": extend})
        return self._create_library_album(resource)

    # Fetch multiple albums from the users library
    @auth_check
    def library_albums(self, ids: List[str], l: str=None, include: List[str]=None, extend: List[str]=None) -> List[LibraryAlbum]:
        resources = self._get_library_resources("albums", {"ids": ids, "l": l, "include": include, "extend": extend})
        return [self._create_library_album(album) for album in resources]

    # Fetch all albums from the users library
    @auth_check
    def all_library_albums(self, l: str=None, include: List[str]=None, extend: List[str]=None) -> List[LibraryAlbum]:
        resources = self._get_library_resources("albums", {"l": l, "include": include, "extend": extend})
        return [self._create_library_album(album) for album in resources]



    # Fetch an artist by its id
    def artist(self, id: str, storefront: str=DEFAULT_STOREFRONT, l: str=None, include: List[str]=None, views: List[str]=None, extend: List[str]=None) -> Artist:
        resource = self._get_catalog_resource("artists", storefront, id, {"l": l, "include": include, "views": views, "extend": extend})
        return self._create_artist(resource)

    # Fetch multiple artists by their ids
    def artists(self, ids: List[str], storefront: str=DEFAULT_STOREFRONT, l: str=None, include: List[str]=None, extend: List[str]=None) -> List[Artist]:
        resources = self._get_catalog_resources("artists", storefront, {"ids": ids, "l": l, "include": include, "extend": extend})
        return [self._create_artist(artist) for artist in resources]

    # Fetch an artist from the users library by its id
    @auth_check
    def library_artist(self, id: str, l: str=None, include: List[str]=None, extend: List[str]=None) -> Optional[LibraryArtist]:
        resource = self._get_library_resource("artists", id, {"l": l, "include": include, "extend": extend})
        return self._create_library_artist(resource)
    
    # Fetch multiple artists from the users library
    @auth_check
    def library_artists(self, ids: List[str], l: str=None, include: List[str]=None, extend: List[str]=None) -> List[LibraryArtist]:
        resources = self._get_library_resources("artists", {"ids": ids, "l": l, "include": include, "extend": extend})
        return [self._create_library_artist(artist) for artist in resources]

    # Fetch all artists from the users library
    @auth_check
    def all_library_artists(self, include: List[str]=None, l: str=None, limit: int=None, offset: str=None, extend: List[str]=None) -> List[LibraryArtist]:
        resources = self._get_library_resources("artists", {"include": include, "l": l, "limit": limit, "offset": offset, "extend": extend})
        return [self._create_library_artist(artist) for artist in resources]



    # Fetch a song by its id
    def song(self, id: str, storefront: str=DEFAULT_STOREFRONT, l: str=None, include: List[str]=None, extend: tr=None) -> Song:
        resource = self._get_catalog_resource("songs", storefront, id, {"l": l, "include": include, "extend": extend})
        return self._create_song(resource)

    # Fetch multiple songs by their ids
    def songs(self, ids: List[str], storefront: str=DEFAULT_STOREFRONT, l: str=None, include: List[str]=None, extend: List[str]=None) -> List[Song]:
        resources = self._get_catalog_resources("songs", storefront, {"ids": ids, "l": l, "include": include, "extend": extend})
        return [self._create_song(song) for song in resources]

    # Fetch a song from the users library by its id
    @auth_check
    def library_song(self, id: str, l: str=None, include: List[str]=None, extend: List[str]=None) -> Optional[LibrarySong]:
        resource = self._get_library_resource("songs", id, {"l": l, "include": include, "extend": extend})
        return self._create_library_song(resource)
    
    # Fetch multiple songs from the users library by their ids
    @auth_check
    def library_songs(self, ids: List[str], l: str=None, include: List[str]=None, extend: List[str]=None) -> List[LibrarySong]:
        resources = self._get_library_resources("songs", {"ids": ids, "l": l, "include": include, "extend": extend})
        return [self._create_library_song(song) for song in resources]
    
    # Fetch all songs from the users library
    @auth_check
    def all_library_songs(self, include: List[str]=None, l: str=None, limit: int=None, offset: str=None, extend: List[str]=None) -> List[LibrarySong]:
        resources = self._get_library_resources("songs", {"include": include, "l": l, "limit": limit, "offset": offset, "extend": extend})
        return [self._create_library_song(song) for song in resources]


    
    # Fetch a music video by its id
    def music_video(self, id: str, storefront: str=DEFAULT_STOREFRONT, l: str=None, include: List[str]=None, views: List[str]=None, extend: List[str]=None) -> MusicVideo:
        resource = self._get_catalog_resource("music-videos", storefront, id, {"l": l, "include": include, "views": views, "extend": extend})
        return self._create_music_video(resource)

    # Fetch multiple music videos by their ids
    def music_videos(self, ids: List[str], storefront: str=DEFAULT_STOREFRONT, l: str=None, include: List[str]=None, views: List[str]=None, extend: List[str]=None) -> List[MusicVideo]:
        resources = self._get_catalog_resources("music-videos", storefront, {"ids": ids, "l": l, "include": include, "views": views, "extend": extend}) 
        return [self._create_music_video(music_video) for music_video in resources]

    # Fetch a music video from the users library by its id
    @auth_check
    def library_music_video(self, id: str, l: str=None, include: List[str]=None, extend: List[str]=None) -> Optional[LibraryMusicVideo]:
        resource = self._get_library_resource("music-videos", id, {"l": l, "include": include, "extend": extend})
        return self._create_library_music_video(resource)

    # Fetch multiple music videos from the users library by their ids
    @auth_check
    def library_music_videos(self, ids: List[str], l: str=None, include: List[str]=None, extend: List[str]=None) -> List[LibraryMusicVideo]:
        resources = self._get_library_resources("music-videos", {"ids": ids, "l": l, "include": include, "extend": extend})
        return [self._create_library_music_video(music_video) for music_video in resources]

    # Fetch all music videos from the users library
    @auth_check
    def all_library_music_videos(self, include: List[str]=None, l: str=None, limit: int=None, offset: str=None, extend: List[str]=None) -> List[LibraryMusicVideo]:
        resources = self._get_library_resources("music-videos", {"include": include, "l": l, "limit": limit, "offset": offset, "extend": extend})
        return [self._create_library_music_video(music_video) for music_video in resources]



    # Fetch a playlist by its id
    def playlist(self, id: str, storefront: str=DEFAULT_STOREFRONT, l: str=None, include: List[str]=None, views: List[str]=None, extend: List[str]=None) -> Playlist:
        resource = self._get_catalog_resource("playlists", storefront, id, {"l": l, "include": include, "views": views, "extend": extend})        
        return self._create_playlist(resource)

    # Fetch multiple playlists by their ids
    def playlists(self, ids: List[str], storefront: str=DEFAULT_STOREFRONT, l: str=None, include: List[str]=None, extend: List[str]=None) -> List[Playlist]:
        resources = self._get_catalog_resources("playlists", storefront, {"ids": ids, "l": l, "include": include, "extend": extend}) 
        return [self._create_playlist(playlist) for playlist in resources]

    # Fetch a playlist from the users library by its id
    @auth_check
    def library_playlist(self, id: str, l: str=None, include: List[str]=None, extend: List[str]=None) -> Optional[LibraryPlaylist]:
        resource = self._get_library_resource("playlists", id, {"l": l, "include": include, "extend": extend})
        return self._create_library_playlist(resource)

    # Fetch multiple playlists from the users library by their ids
    @auth_check
    def library_playlists(self, ids: List[str], l: str=None, include: List[str]=None, extend: List[str]=None) -> List[LibraryPlaylist]:
        resources = self._get_library_resources("playlists", {"ids": ids, "l": l, "include": include, "extend": extend})
        return [self._create_library_playlist(playlist) for playlist in resources]
    
    # Fetch all playlists from the users library
    @auth_check
    def all_library_playlists(self, include: List[str]=None, l: str=None, limit: int=None, offset: str=None, extend: List[str]=None) -> List[LibraryPlaylist]:
        resources = self._get_library_resources("playlists", {"include": include, "l": l, "limit": limit, "offset": offset, "extend": extend})
        return [self._create_library_playlist(playlist) for playlist in resources]

    
    
    # Fetch a music station by its id
    def station(self, id: str, storefront: str=DEFAULT_STOREFRONT, include: List[str]=None, l: str=None, extend: List[str]=None) -> Station:
        resource = self._get_catalog_resource("stations", storefront, id, {"l": l, "include": include, "extend": extend}) 
        return self._create_station(resource)
    
    # Fetch multiple music stations by their ids
    def stations(self, ids: List[str], storefront: str=DEFAULT_STOREFRONT, include: List[str]=None, l: str=None, extend: List[str]=None) -> List[Station]:
        resources = self._get_catalog_resources("stations", storefront, {"ids": ids, "l": l, "include": include, "extend": extend})
        return [self._create_station(station) for station in resources]

    # Fetch a station genre by its id
    def station_genre(self, id: str, storefront: str=DEFAULT_STOREFRONT, include: List[str]=None, l: str=None, extend: List[str]=None) -> StationGenre:
        resource = self._get_catalog_resource("station-genres", storefront, id, {"l": l, "include": include, "extend": extend})
        return self._create_station_genre(resource)
    
    # Fetch multiple station genres by their ids
    def station_genres(self, ids: List[str], storefront: str=DEFAULT_STOREFRONT, include: List[str]=None, l: str=None, extend: List[str]=None) -> List[StationGenre]:
        resources = self._get_catalog_resources("station-genres", storefront, {"ids": ids, "l": l, "include": include, "extend": extend})
        return [self._create_station_genre(station_genre) for station_genre in resources]
    
    # Fetch top station genres
    def top_station_genres(self, storefront: str=DEFAULT_STOREFRONT, include: List[str]=None, l: str=None, limit: int=None, offset: str=None, extend: List[str]=None) -> List[StationGenre]:
        resource = self._get_catalog_resources("station-genres", storefront, {"l": l, "include": include, "limit": limit, "offset": offset, "extend": extend}) 
        return self._create_station_genre(resource)

    # Fetch a genre by its id
    def genre(self, id: str, storefront: str=DEFAULT_STOREFRONT, include: List[str]=None, l: str=None, extend: List[str]=None) -> Genre:
        resource = self._get_catalog_resource("genres", storefront, id, {"l": l, "include": include, "extend": extend})
        return self._create_genre(resource)

    # Fetch multiple genres by their ids
    def genres(self, ids: str, storefront: str=DEFAULT_STOREFRONT, l: str=None, include: List[str]=None, extend: List[str]=None) -> List[Genre]:
        resources = self._get_catalog_resources("genres", storefront, {"ids": ids, "l": l, "include": include, "extend": extend})
        return [self._create_genre(genre) for genre in resources]
    
    # Fetch top genre from charts
    def top_genres(self, storefront: str=DEFAULT_STOREFRONT, l: str=None, limit: int=None, offset: str=None, include: List[str]=None, extend: List[str]=None) -> List[Genre]:
        resources = self._get_catalog_resources("genres", storefront, {"l": l, "limit": limit, "offset": offset, "include": include, "extend": extend}) 
        return [self._create_genre(genre) for genre in resources]


    # Fetch charts
    def charts(self, storefront: str=DEFAULT_STOREFRONT, types: List[str]=None, l: str=None, chart: str=None, genre: str=None, limit: int=None, offset: str=None) -> List[Chart]:
        resources = self._get_catalog_resources("charts", storefront, {"l": l, "chart": chart, "genre": genre, "limit": limit, "offset": offset})
        return [self._create_chart(chart) for chart in resources]

    # Fetch an activity by its id
    def activity(self, id: str, storefront: str=DEFAULT_STOREFRONT, l: str=None, include: List[str]=None, extend: List[str]=None) -> Activity:
        resource = self._get_catalog_resource("activities", storefront, id, {"l": l, "include": include, "extend": extend})
        return self._create_activity(resource)

    # Fetch multiple activities by their ids
    def activities(self, ids: List[str], storefront: str=DEFAULT_STOREFRONT, include: List[str]=None, l: str=None, extend: List[str]=None) -> List[Activity]:
        resources = self._get_catalog_resources("activities", storefront, {"ids": ids, "l": l, "include": include, "extend": extend})
        return [self._create_activity(activity) for activity in resources]

    # Fetch curator by its id
    def curator(self, id: str, storefront: str=DEFAULT_STOREFRONT, l: str=None, include: List[str]=None, extend: List[str]=None) -> Curator:
        resource = self._get_catalog_resource("curators", storefront, id, {"l": l, "include": include, "extend": extend})
        return self._create_curator(resource)
    
    # Fetch multiple curators by their ids
    def curators(self, ids: List[str], storefront: str=DEFAULT_STOREFRONT, include: List[str]=None, l: str=None, extend: List[str]=None) -> List[Curator]:
        resources = self._get_catalog_resources("curators", storefront, {"ids": ids, "l": l, "include": include, "extend": extend})
        return [self._create_curator(curator) for curator in resources]

    # Fetch apple curator by its id
    def apple_curator(self, id: str, storefront: str=DEFAULT_STOREFRONT, l: str=None, include: List[str]=None, extend: List[str]=None) -> AppleCurator:
        resource = self._get_catalog_resource("apple-curators", storefront, id, {"l": l, "include": include, "extend": extend})
        return self._create_apple_curator(resource)

    # Fetch multiple apple curators by their ids
    def apple_curators(self, ids: List[str], storefront: str=DEFAULT_STOREFRONT, include: List[str]=None, l: str=None, extend: List[str]=None) -> List[AppleCurator]:
        resources = self._get_catalog_resources("apple-curators", storefront, {"ids": ids, "l": l, "include": include, "extend": extend})
        return [self._create_apple_curator(curator) for curator in resources]

    # Fetch record label by its id
    def record_label(self, id: str, storefront: str=DEFAULT_STOREFRONT, extend: List[str]=None, include: List[str]=None, l: str=None, views: List[str]=None) -> RecordLabel:
        resource = self._get_catalog_resource("record-labels", storefront, id, {"l": l, "extend": extend, "include": include, "views": views}) 
        return self._create_record_label(resource)

    # Fetch multiple record labels by their ids
    def record_labels(self, ids: List[str], storefront: str=DEFAULT_STOREFRONT, extend: List[str]=None, include: List[str]=None, l: str=None) -> List[RecordLabel]:
        resources = self._get_catalog_resources("record-labels", storefront, {"ids": ids, "l": l, "extend": extend, "include": include})
        return [self._create_record_label(record_label) for record_label in resources]

    # Fetch recommendation by its id
    def recommendation(self, id: str, storefront: str=DEFAULT_STOREFRONT, l: str=None, include: List[str]=None, extend: List[str]=None) -> Recommendation:
        resource = self._get_catalog_resource("recommendations", storefront, id, {"l": l, "include": include, "extend": extend}) 
        return self._create_recommendation(resource)

    # Fetch multiple recommendations by their ids
    def recommendations(self, ids: List[str], storefront: str=DEFAULT_STOREFRONT, l: str=None, include: List[str]=None, extend: List[str]=None) -> List[Recommendation]:
        resources = self._get_catalog_resources("recommendations", storefront, {"ids": ids, "l": l, "include": include, "extend": extend})
        return [self._create_recommendation(recommendation) for recommendation in resources]
    
    # Fetch default recommendations
    def default_recommendations(self, storefront: str=DEFAULT_STOREFRONT, l: str=None, limit: int=None, offset: str=None, include: List[str]=None, extend: List[str]=None) -> List[Recommendation]:
        resources = self._get_catalog_resources("recommendations", storefront, {"l": l, "limit": limit, "offset": offset, "include": include, "extend": extend})
        return [self._create_recommendation(recommendation) for recommendation in resources]

    
    # Search for a catalog resource
    def search(self, storefront: str=DEFAULT_STOREFRONT, term: str=None, l: str=None, limit: int=None, offset: str=None, types: List[str]=None, qwith: List[str]=None) -> SeachResults:
        resources = self._get_catalog_resources("search", storefront, {"term": term, "l": l, "limit": limit, "offset": offset, "types": types, "with": qwith})
        return self._create_search_results(resources)


    # Search for a library resource
    def library_search(self, term: str=None, types: List[str]=None, limit: int=None, offset: str=None, l: str=None) -> LibrarySearchResults:
        resources = self._get_library_resources("search", {"term": term, "types": types, "limit": limit, "offset": offset, "l": l})
        return self._create_library_search_results(resources)