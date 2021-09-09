class Page:

    def __init__(self, title: str, url: str, page_id: str, level: int, ancestors: list, body_size: int):
        self.url = url
        self.id = page_id
        self.title = title
        self.level = level
        self.ancestors = ancestors
        self.body_size = body_size


    @classmethod
    def from_dict(cls, page_as_dict: dict) -> 'Page':
        if page_as_dict.get('body', False):
            body_size = len(page_as_dict["body"]["storage"]["value"])
        else:
            body_size = 0

        return cls(title=page_as_dict['title'],
                   url=page_as_dict['_links']['webui'],
                   page_id=page_as_dict["id"],
                   level=len(page_as_dict['ancestors']),
                   ancestors=[ancestor['id'] for ancestor in page_as_dict['ancestors']],
                   body_size=body_size
                   )


    def __str__(self):
        return self.title + ' - ' + self.url
