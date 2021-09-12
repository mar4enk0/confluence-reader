import re
import xml.etree.ElementTree as ET


class Page:

    def __init__(self, title: str, url: str, page_id: str, level: int, ancestors: list, body: str):
        self.url = url
        self.page_id = page_id
        self.title = title
        self.level = level
        self.ancestors = ancestors
        self.body = body


    @classmethod
    def from_dict(cls, page_as_dict: dict) -> 'Page':
        if page_as_dict.get('body', False):
            body = page_as_dict["body"]["storage"]["value"]
        else:
            body = ''
        return cls(title=page_as_dict['title'],
                   url=page_as_dict['_links']['webui'],
                   page_id=page_as_dict["id"],
                   level=len(page_as_dict['ancestors']),
                   ancestors=[ancestor['id'] for ancestor in page_as_dict['ancestors']],
                   body=body
                   )


    @property
    def body(self):
        return self._body


    @body.setter
    def body(self, body: str):
        if len(body) == 0:
            self._body = ''
            self.body_size = 0
            return

        template = '<confluence>{0}</confluence>'
        body = body.replace('ac:', '').replace('ri:', '').replace('&', '')

        result = re.findall('&.*?;', body)
        if result:
            for e in frozenset(result):
                body = body.replace(e, '')

        body = template.format(body)

        elems_to_delete = ['.//structured-macro[@macro-id="fa9c0aba-be69-4a80-9761-d13f04399718"]',
                           './/structured-macro[@macro-id="611cb948-bc44-4d24-9650-cb6ed1dff555"]',
                           './/structured-macro[@macro-id="2f286453-8317-40fb-83d6-7987d3acc62e"]',
                           './/structured-macro[@macro-id="1a2b75f9-f881-4e55-af69-d7614115756d"]',
                           './/structured-macro[@macro-id="a29ae77c-c1d8-43df-aced-4419910c9186"]',
                           './/structured-macro[@macro-id="a944ee95-4595-4dd1-b42b-719a5ebcf06d"]',
                           './/structured-macro[@macro-id="4219a0e5-475e-406b-aba6-7c463536313a"]',
                           './/structured-macro[@macro-id="3555d197-4165-40ff-9889-7e2edb8cfda7"]/rich-text-body/table']

        root = ET.fromstring(body)
        for e in elems_to_delete:
            elem = root.find(e)
            elem_parent = root.find(e + '/..')
            if elem and elem_parent:
                elem_parent.remove(elem)

        body = ET.tostring(root, encoding="unicode")

        self._body = body
        self.body_size = 0 if (len(body) - 330) < 0 else len(body) - 330


    def __str__(self):
        return self.title + ' - ' + self.url
