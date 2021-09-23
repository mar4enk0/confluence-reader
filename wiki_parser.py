import csv
import json

import requests

from page import Page
from settings import WIKI_URL, HEADERS, REST_URL


def get_page_version(page_id: str):
    full_url = REST_URL + '/' + page_id
    r = requests.get(full_url, headers=HEADERS, timeout=10)
    version = r.json()['version']['number']
    return version


def get_pages(cql: str, url: str):
    full_url = url.format(cql)

    # Get that passes in the space and expands the ancestors
    r = requests.get(full_url, headers=HEADERS, timeout=10)
    if r.status_code != 200:
        raise Exception(r.content)

    pages = r.json()['results'][:]

    while True:
        try:
            next_page = r.json()['_links']['next']
            full_url = WIKI_URL + next_page
            r = requests.get(full_url, headers=HEADERS)

            pages.extend(r.json()['results'][:])
        except KeyError:
            break

    return pages


def sort_pages(page_objs):
    # Add pages to a list based on their hierarchy and parent
    sorted_pages = []
    page_levels = max(page.level for page in page_objs)
    for level in range(page_levels + 1):
        if level == 0:
            # First add pages at the root level of the space
            sorted_pages.extend([page for page in page_objs if page.level == 0])

        else:
            # Create list of pages at the current level
            children = [page for page in page_objs if page.level == level]
            # Create a list of parent pages for the children
            parents = [page for page in sorted_pages if page.level == level - 1]
            for page in children:
                for pg in parents:
                    # Check whether the parent ID is in the child's ancestors and put the child after the parent if so.
                    if pg.page_id in page.ancestors:
                        try:
                            sorted_pages.insert(sorted_pages.index(pg) + 1, page)
                            continue
                        except ValueError:
                            print(pg.title + ' caused an error')
                    # else:
                    #     continue

    sorted_pages.extend([p for p in page_objs if p not in sorted_pages])

    # for page in page_objs:
    #     if page not in sorted_pages:
    #         sorted_pages.append(page)

    return sorted_pages


def write_pages_to_csv(pages, file_name):
    page_levels = max(page.level for page in pages)
    with open(f'./out/{file_name}', mode='w', newline='') as levels:
        fieldnames = [f'Level {level}' for level in range(page_levels + 1)]
        fieldnames.append('URL')
        fieldnames.append('body_size')

        writer = csv.DictWriter(levels, fieldnames=fieldnames)
        writer.writeheader()

        for page in pages:
            link = WIKI_URL + page.url
            row_dict = {f'Level {page.level}': page.title, 'URL': link, 'body_size': page.body_size}
            writer.writerow(row_dict)


def transform_to_page_objects(pages, sort: bool = False):
    page_objs = []
    for page in pages:
        pg = Page.from_dict(page)
        page_objs.append(pg)
    if sort:
        return sort_pages(page_objs)
    else:
        return page_objs


def generate_cvs(params: dict):
    pages = get_pages(params['cql'], params['url'])
    if len(pages) == 0:
        raise Exception("No pages found. Please check your query.")

    page_objs = transform_to_page_objects(pages, params['sort'])
    write_pages_to_csv(page_objs, params['file_name'])


def update_page(page_id: str, data: str, version: int, quality_title: str):
    full_url = REST_URL + '/' + page_id

    d = {"id": page_id,
         "type": "page",
         "title": quality_title,
         "space": {"key": "ACP"},
         "body": {"storage":
                      {"value": data,
                       "representation": "storage"}},
         "version": {"number": version}
         }

    r = requests.put(full_url, data=json.dumps(d), headers=HEADERS, timeout=10)
    if r.status_code != 200:
        raise Exception(r.content)


def update_stats_page(params):
    version = get_page_version(params['quality_page_id'])
    pages = get_pages(params['cql'], params['url'])
    page_objs = transform_to_page_objects(pages)

    table_template = '''
    <table data-layout=\"full-width\" ac:local-id=\"ca786083-6227-4a4c-ae32-7d962fe83583\">
        <colgroup>
            <col style=\"width: 400px;\"/>
            <col style=\"width: 400px;\"/>
            <col style=\"width: 135px;\"/>
            <col style=\"width: 65px;\"/>
        </colgroup>
        <thead>
            <tr>
                <th><strong>Title</strong></th>
                <th><strong>Link</strong></th>
                <th><strong>Owner(s)</strong></th>
                <th><strong>Quality</strong></th>
            </tr>
        </thead>
        <tbody>{0}</tbody>
    </table>'''

    quality_dic = {
        'Very Poor': 'Grey',
        'Poor': 'Red',
        'Fair': 'Yellow',
        'Good': 'Blue',
        'Excellent': 'Green'
    }

    quality_template = '''
    <ac:structured-macro ac:name=\"status\" ac:schema-version=\"1\" ac:macro-id=\"207a0de3-0db7-4eb3-845d-af7eeaf11074\">
	    <ac:parameter ac:name=\"title\">{0}</ac:parameter>
		<ac:parameter ac:name=\"colour\">{1}</ac:parameter>
	</ac:structured-macro>'''

    link_template = '''
    <ac:link ac:card-appearance=\"inline\">
	    <ri:page ri:content-title=\"{0}\"/>
		<ac:link-body>{0}</ac:link-body>
	</ac:link>'''

    user_template = '''
<ac:link>
<ri:user ri:userkey="{0}"/>
</ac:link>'''

    row_template = '<tr><td><p>{0}</p></td><td><p>{1}</p></td><td><p>{2}</p></td><td><p>{3}</p></td></tr>\n'
    rows = []

    for page in page_objs:
        quality = quality_template.format(page.quality, quality_dic.get(page.quality, 'Grey'))
        link = link_template.format(page.title)  #
        owners = [user_template.format(u) for u in page.users]
        row = row_template.format(page.title, link, "".join(owners), quality)  # WIKI_URL + page.url
        rows.append(row)

    table = ''.join(rows)
    table = table_template.format(table)
    table = table.replace('\n', '').replace('\t', '').replace('&', '&amp;')
    print(table)
    update_page(params['quality_page_id'], table, version + 1, params['quality_title'])
