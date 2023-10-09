import requests
import json
from itertools import islice

token = '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'
base_url = 'https://api.github.com'
headers = {'Authorization': f'token {token}'}


def get_pull_requests(owner, repo):
    url = f'{base_url}/repos/{owner}/{repo}/pulls'
    params = {'state': 'all', 'per_page': 10, 'page': 1}
    pull_requests = []

    while True:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            pr_data = response.json()
            if not pr_data:
                break
            pull_requests.extend(pr_data)
            params['page'] += 1
        else:
            print(f'Erro ao buscar pull requests do repositório {owner}/{repo}: {response.status_code}')
            break

    return pull_requests[:1000]


def save_pull_requests_to_json(owner, repo, pull_requests):
    filename = f'{owner}_{repo}_pull_requests.json'
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(pull_requests, file, indent=4)


def get_popular_repositories():
    url = f'{base_url}/search/repositories'
    params = {'q': 'stars:>0', 'sort': 'stars', 'order': 'desc', 'per_page': 10, 'page': 1}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        repositories_data = response.json()['items']
        return repositories_data
    else:
        print(f'Erro ao buscar repositórios populares: {response.status_code}')
        return []

popular_repositories = get_popular_repositories()
for repo_data in popular_repositories:
    owner = repo_data['owner']['login']
    repo = repo_data['name']
    pull_requests = get_pull_requests(owner, repo)
    save_pull_requests_to_json(owner, repo, pull_requests)
    print(f'Pull requests salvas para {owner}/{repo}')

print('Concluído.')
