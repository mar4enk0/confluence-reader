from wiki_parser import generate_report

tech_practice = {
    'cql': 'space = "ACP" AND type = page AND label="tech-practice" AND label!="project-page"',
    'url': '/rest/api/content/search?cql={0}&start=0&limit=50&expand=ancestors,body.storage',
    'file_name': 'ACP_tech_practice_quality.csv',
    'sort': False
}


db_practice = {
    'cql': 'space = "ACP" AND type = page AND label="db-practice" AND label!="project-page"',
    'url': '/rest/api/content/search?cql={0}&start=0&limit=50&expand=ancestors,body.storage',
    'file_name': 'ACP_tech_practice_quality.csv',
    'sort': False
}

ACP_hierarchy = {
    'cql': 'space = "ACP" AND type = page',
    'url': '/rest/api/content/search?cql={0}&start=0&limit=50&expand=ancestors',
    'file_name': 'ACP_hierarchy.csv',
    'sort': True
}

customer_projects_hierarchy = {
    'cql': 'space = "ACP" AND type = page AND ancestor = 26247178',
    'url': '/rest/api/content/search?cql={0}&start=0&limit=50&expand=ancestors',
    'file_name': 'customer_projects_hierarchy.csv',
    'sort': True
}


generate_report(customer_projects_hierarchy)