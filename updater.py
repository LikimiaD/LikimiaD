import requests
import os

def grid_data(username):
    token = os.getenv('MY_TOKEN')
    headers = {'Authorization': f'token {token}'}

    repos_response = requests.get(f'https://api.github.com/users/{username}/repos?type=owner&per_page=100', headers=headers)
    
    if repos_response.status_code == 200:
        repos = repos_response.json()
    else:
        print(f"Error fetching repos: {repos_response.status_code}")
        print(repos_response.text)
        exit()

    total_stars = sum(repo['stargazers_count'] for repo in repos)
    
    sorted_repos = sorted(repos, key=lambda x: x['created_at'], reverse=True)[:5]
    repo_names_languages = [(repo['name'], repo['language']) for repo in sorted_repos]

    total_commits = 0
    for repo in repos:
        commits_url = repo['commits_url'].split('{')[0]  # Удаление {/sha} из URL
        commits_response = requests.get(commits_url, headers=headers)
        commits_count = len(commits_response.json())
        total_commits += commits_count

    return total_stars, total_commits, repo_names_languages

def update_readme(username, stats):
    total_stars, total_commits, repo_names_languages = stats
    avatar = os.getenv('MY_AVATAR')

    readme_content = f"""
```zsh
> neofetch
```

<img align="left" src="{avatar}" alt="LikimiaD Github Avatar" width="350" height="350" /> 

```
likimiad@github
-------------------------
Name: Igor
Main Education: National University of Science and Technology MISIS
Additional education: School21 (Moscow Campus) *In EU called School42*
Pronouns: He/Him
Location: Moscow, Russia
Frameworks: Django, Flask, Numpy,
            Pandas, Sklearn, openCV,
            aiogram, Qt
Languages: Python, C, C++, C#, SQL
Learning: JS, Golang, C++
Hobbies: SIM Racing, Reverse engineering, Cycling
Commits: {total_commits}
Stars: {total_stars}
Discord: likimiad
```
<p align="left">
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp;
<img alt="#474342" src="https://via.placeholder.com/15/474342/000000?text=+" width="25" height="20" /><img alt="#fbedf6" src="https://via.placeholder.com/15/fbedf6/000000?text=+" width="25" height="20" /><img alt="#676767" src="https://via.placeholder.com/15/676767/000000?text=+" width="25" height="20" /><img alt="#181818" src="https://via.placeholder.com/15/181818/000000?text=+" width="25" height="20" /><img alt="#ae9c9d" src="https://via.placeholder.com/15/ae9c9d/000000?text=+" width="25" height="20" />
</p>

```zsh
> git log -n 5
```

```
Last Projects:
"""

    for name, language in repo_names_languages:
        readme_content += f"{'Project name:':<13} {name}\n{'Language:':<13} {language}\n"
        
    readme_content += """```
```zsh
> openssl s_client -connect likimiad:443 -servername -showcerts
```
### Certificates:

**Udemy** -> Python Course [RU](https://drive.google.com/file/d/1qQL9Emr5hgZaehdFBfGmX9Ecda__gQtU/view?usp=sharing)

**Yandex** -> Young&&Yandex Algorithm Training 3.0 [RU](https://drive.google.com/file/d/1C3WHKdxITHBoZWk6WRuJoRcB1LgqNXdq/view?usp=sharing)

**Karpov.Courses** -> Docker Course [RU](https://lab.karpov.courses/certificate/27aa9384-171e-41d5-b6fb-8022047cbfb1/) [EN](https://lab.karpov.courses/certificate/27aa9384-171e-41d5-b6fb-8022047cbfb1/en/)

**Karpov.Courses** -> SQL Simulator [RU](https://lab.karpov.courses/certificate/40b96305-67b3-422e-bd90-6bed7f1404ab/) [EN](https://lab.karpov.courses/certificate/40b96305-67b3-422e-bd90-6bed7f1404ab/en/)
"""

    with open('README.md', 'w') as readme_file:
        readme_file.write(readme_content)


if __name__ == "__main__":
    username = 'LikimiaD'
    repo_names_languages = grid_data(username)
    update_readme(username, repo_names_languages)