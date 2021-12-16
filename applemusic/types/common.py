from typing import Optional

class Artwork:
    """
    bgColor: The average background color of the image.: string
    height: The maximum height of the image in pixels.: integer
    width: The maximum width of the image in pixels.: integer
    textColor1: The primary text color of the image.: string
    textColor2: The secondary text color of the image.: string
    textColor3: The tertiary text color of the image.: string
    textColor4: The quaternary text color of the image.: string
    url: The URL to request the image asset. {w}x{h}must precede image filename, as placeholders for the width and height values as described above. For example, {w}x{h}bb.jpeg).: string 
    """
    def __init__(self, data):
        self.bgColor: str = data.get('bgColor')
        self.height: int = data.get('height')
        self.width: int = data.get('width')
        self.textColor1: str = data.get('textColor1')
        self.textColor2: str = data.get('textColor2')   
        self.textColor3: str = data.get('textColor3')
        self.textColor4: str = data.get('textColor4')
        self.url: str = data.get('url')

class Preview:
    def __init__(self, data):
        self.arwork: Optional[Artwork] = Artwork(data.get('artwork')) if data.get('artwork') else None
        self.url: str = data.get('url')
        self.hlsUrl: str = data.get('hlsUrl')

class EditorialNotes:
    """
    short: The short editorial notes.: string
    standard: The standard editorial notes.: string
    name: The name of the editorial notes.: string
    tagline: The tagline of the editorial notes.: string
    """
    def __init__(self, data):
        self.short: str = data.get('short')
        self.standard: str = data.get('standard')
        self.name: str = data.get('name')
        self.tagline: str = data.get('tagline')

class PlayParameters:
    """
    id: The ID of the play parameter.: string
    kind: The kind of the play parameter. Always art-play-parameter for art play parameters.: string
    """
    def __init__(self, data):
        self.id: str = data.get('id')
        self.kind: str = data.get('kind')