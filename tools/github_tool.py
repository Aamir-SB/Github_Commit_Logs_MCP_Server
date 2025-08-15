import subprocess
import requests
import logging
from datetime import datetime

# Define the full format string for commit date
date_format = "%a %b %d %H:%M:%S %Y %z"

def get_git_commits():
    # Run the git command to get commit history
    result = subprocess.run(['git', 'log', '--pretty=format:%H -- %s -- %cd'], capture_output=True, text=True)
    
    # Parse the result into a list of commits
    commits = []
    for line in result.stdout.splitlines():
        commit_hash, message, date = line.split(' -- ', 2)
        commits.append({
            "hash": commit_hash,
            "message": message,
            "date": date
        })
        
    # return commits
    return [generate_bullet_points(commit, include_hash=False) for commit in commits]


# Function to parse the commit date and extract just the time in 12-hour format with AM/PM
def parse_commit_time(date_string):
    try:
        # Parse the full datetime string
        parsed_date = datetime.strptime(date_string, date_format)
        # Extract just the time part in 12-hour format with AM/PM
        return parsed_date.strftime("%I:%M:%S %p")  # Format to 'HH:MM:SS AM/PM'
    except ValueError as e:
        print(f"Error parsing date: {e}")
        return None

# Function to format the commit into a bullet point
def generate_bullet_points(commit, include_hash=True):
    commit_time = parse_commit_time(commit["date"])
    if commit_time:
        if include_hash:
            # Bullet point with commit hash
            bullet_point = f"- [{commit['hash'][:7]}] {commit['message']} (committed at {commit_time})"
        else:
            # Bullet point without commit hash
            bullet_point = f"- {commit['message']} (committed at {commit_time})"
    return bullet_point
        

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