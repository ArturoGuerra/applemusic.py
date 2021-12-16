from typing import Optional, List

class GenresAttributes:
    """
    name: str
    parentId: Optional[str]
    parentName: Optional[str]
    """
    def __init__(self, data):
        self.name: str = data.get('name')
        self.parentId: Optional[str] = data.get('parentId', None)
        self.parentName: Optional[str] = data.get('parentName', None)   

class Genre:
    """
    id: str
    href: str
    attributes: GenresAttributes
    """
    def __init__(self, data):
        self.id: str = data.get('id', None)
        self.href: str = data.get('href', None)
        self.attributes: Optional[GenresAttributes] = GenresAttributes(data.get('attributes')) if data.get('attributes', None) else None

class GenresRelationship:
    """
    href: str
    next: str
    data: List[Genre]
    """
    def __init__(self, data):
        self.href: str = data.get('href')
        self.next: str = data.get('next')
        self.data: List[Genre] = [Genre(d) for d in data.get('data')]