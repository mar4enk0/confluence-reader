import csv
import requests
from page import Page
from settings import TOKEN, SITE


# HIERARCHY_CQL = f'space = {SPACE} AND type = page'
# HIERARCHY_URL = SITE + f'/rest/api/content/search?cql={cql}&start=0&limit=50&expand=ancestors'


def get_pages(cql: str, url: str):
    headers = {
        "Authorization": "Basic " + TOKEN,
        "Content-Type": "application/json"
    }

    url = SITE + url.format(cql)
    pages = []

    # Get that passes in the space and expands the ancestors
    r = requests.get(url, headers=headers, timeout=10)

    page_list = r.json()['results']
    for page in page_list:
        pages.append(page)

    is_next_page = True

    while is_next_page:
        try:
            next_page = r.json()['_links']['next']
            url = SITE + next_page
            r = requests.get(url, headers=headers)

            page_list = r.json()['results']
            for page in page_list:
                pages.append(page)
        except KeyError:
            is_next_page = False

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
                    if pg.id in page.ancestors:
                        try:
                            sorted_pages.insert(sorted_pages.index(pg) + 1, page)
                            continue
                        except ValueError:
                            print(pg.title + ' caused an error')
                    else:
                        continue
    for page in page_objs:
        if page not in sorted_pages:
            sorted_pages.append(page)

    return sorted_pages


def write_pages_to_csv(pages, file_name):
    page_levels = max(page.level for page in pages)
    with open(f'./{file_name}', mode='w', newline='') as levels:

        fieldnames = [f'Level {level}' for level in range(page_levels + 1)]
        fieldnames.append('URL')
        fieldnames.append('body_size')

        writer = csv.DictWriter(levels, fieldnames=fieldnames)
        writer.writeheader()

        for page in pages:
            link = SITE + page.url
            row_dict = {f'Level {page.level}': page.title, 'URL': link, 'body_size': page.body_size}
            writer.writerow(row_dict)


def generate_report(params: dict):
    pages = get_pages(params['cql'], params['url'])
    page_objs = []
    for page in pages:
        pg = Page.from_dict(page)
        page_objs.append(pg)
    if params['sort']:
        sorted_pages = sort_pages(page_objs)
        write_pages_to_csv(sorted_pages, params['file_name'])
    else:
        write_pages_to_csv(page_objs, params['file_name'])
