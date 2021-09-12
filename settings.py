#create your personal token here: https://id.atlassian.com/manage-profile/security/api-tokens
TOKEN = ''
WIKI_URL = 'https://akvelon.atlassian.net/wiki'
REST_URL = WIKI_URL + '/rest/api/content'

HEADERS = {
    "Authorization": "Basic " + TOKEN,
    "Content-Type": "application/json"
}

tech_practice = {
    'cql': 'space = "ACP" AND type = page AND label="tech-practice" \
           AND label NOT IN ("project-page", \
                            "case-study", \
                            "tech-db-root-practice", \
                            "tech-data-science-root-practice", \
                            "tech-cloud-root-practice", \
                            "tech-data-analytics-root-practice", \
                            "tech-data-engineering-root-practice", \
                            "tech-desktop-root-practice", \
                            "tech-devops-root-practice", \
                            "tech-frontend-root-practice", \
                            "tech-general-root-practice", \
                            "tech-mobile-root-practice", \
                            "tech-qa-root-practice", \
                            "tech-security-root-practice", \
                            "tech-ux-ui-root-practice", \
                            "tech-ar-vr-root-practice" \
                            )',
    'url': REST_URL + '/search?cql={0}&start=0&limit=50&expand=ancestors,body.storage',
    'file_name': 'ACP_tech_practice_quality.csv',
    'sort': False
}

db_practice = {
    'cql': 'space = "ACP" AND type = page AND label="tech-db" \
            AND label NOT IN ("project-page", "tech-db-root-practice")',
    'url': REST_URL + '/search?cql={0}&start=0&limit=50&expand=ancestors,body.storage',
    'file_name': 'ACP_db_practice_quality.csv',
    'quality_page_id': '1498415544',
    'sort': False
}

ml_practice = {
    'cql': 'space = "ACP" AND type = page AND label in ("tech-data-science", "tech-machine-learning") \
            AND label NOT IN ("project-page", "case-study", "tech-data-science-root-practice")',
    'url': REST_URL + '/search?cql={0}&start=0&limit=50&expand=ancestors,body.storage',
    'file_name': 'ACP_ml_practice_quality.csv',
    'sort': False
}

ACP_hierarchy = {
    'cql': 'space = "ACP" AND type = page',
    'url': REST_URL + '/search?cql={0}&start=0&limit=50&expand=ancestors',
    'file_name': 'ACP_hierarchy.csv',
    'sort': True
}

customer_projects_hierarchy = {
    'cql': 'space = "ACP" AND type = page AND ancestor = 26247178',
    'url': REST_URL + '/search?cql={0}&start=0&limit=50&expand=ancestors',
    'file_name': 'customer_projects_hierarchy.csv',
    'sort': True
}
