import subprocess
import requests


def get_git_commits():
    # Run the git command to get commit history
    result = subprocess.run(['git', 'log', '--pretty=format:%H %s %cd'], capture_output=True, text=True)
    
    # Parse the result into a list of commits
    commits = []
    for line in result.stdout.splitlines():
        commit_hash, message, date = line.split(' ', 2)
        commits.append({
            "hash": commit_hash,
            "message": message,
            "date": date
        })
    return commits


# Function to post work logs to API
def post_work_log(api_url, token, commit):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    data = {
        'date': commit['date'],
        'description': commit['message'],
        'hours': 1  # Placeholder for the amount of time spent
    }

    response = requests.post(api_url, json=data, headers=headers)

    if response.status_code == 201:
        print(f"Successfully posted work log: {commit['message']}")
    else:
        print(f"Failed to post work log: {response.status_code}")