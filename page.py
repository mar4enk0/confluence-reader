import xml.etree.ElementTree as ET


class Page:
    quality_dic = (
        (0, 500, 'Very Poor'),
        (501, 2_300, 'Poor'),
        (2_301, 4_000, 'Fair'),
        (4_001, 9_000, 'Good'),
        (9_001, 100_000, 'Excellent')
    )

    def __init__(self, title: str, url: str, page_id: str, level: int, ancestors: list, body: str):
        self.url = url
        self.page_id = page_id
        self.title = title
        self.level = level
        self.ancestors = ancestors
        self._quality = 'Undefined'
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
    def quality(self):
        return self._quality


    @quality.setter
    def quality(self, body_size: int):
        for low, high, q in Page.quality_dic:
            if low <= body_size <= high:
                self._quality = q
                return


    @property
    def body(self):
        return self._body


    @body.setter
    def body(self, body: str):
        if len(body) == 0:
            self._body = ''
            self.body_size = 0
            self.quality = 0
            return

        template = '<confluence>{0}</confluence>'
        body = body.replace('ac:', '').replace('ri:', '').replace('&', '')

        # body = re.sub('&.*?;', '', body)
        # result = re.findall('&.*?;', body)
        # if result:
        #     for e in frozenset(result):
        #         body = body.replace(e, '')

        body = template.format(body)

        elems_to_delete = [
            './/structured-macro[@name="note"]',
            './/structured-macro[@name="info"]'
        ]

        root: ET.Element = ET.fromstring(body)
        for e in elems_to_delete:
            elems_found = root.findall(e)
            for elem in elems_found:
                elem_parent = root.find(e + '/..')
                if elem and elem_parent:
                    elem_parent.remove(elem)

        el: ET.Element = root.findall('.//user')
        self.users = []
        if el is not None and len(el) > 0:
            self.users = list(set([e.attrib['userkey'] for e in el]))

        body = ET.tostring(root, encoding="unicode")

        self._body = body
        self.body_size = 0 if (len(body) - 831) < 0 else len(body) - 831
        self.quality = self.body_size

    def __str__(self):
        return self.title + ' - ' + self.url
