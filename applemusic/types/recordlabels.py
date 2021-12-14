from typing import List

class DescriptionAttrbute:
    """
    short: str
    standard: str
    """
    def __int__(self, data):
        self.short: str = data.get('short')
        self.standard: str = data.get('standard')
        
class RecordLabelAttributes:
    """
    artwork: Artwork
    description: str
    name: str
    url: str
    """
    def __init__(self, data):
        self.artwork: Artwork = Artwork(data.get('artwork'))
        self.description: DescriptionAttrbute = DescriptionAttrbute(data.get('description'))
        self.name: str = data.get('name')
        self.url: str = data.get('url')

class RecordLabel:
    """
    id: str
    href: str
    attributes: RecordLabelAttributes
    """
    def __init__(self, data):
        self.id: str = data.get('id')
        self.href: str = data.get('href')
        self.attributes: RecordLabelAttributes = RecordLabelAttributes(data.get('attributes'))

class RecordLabelsRelationship:
    """
    href: str
    next: str
    data: List[RecordLabel]
    """
    def __init__(self, data):
        self.href: str = data.get('href')
        self.next: str = data.get('next')
        self.data: List[RecordLabel] = [RecordLabel(item) for item in data.get('data')] 