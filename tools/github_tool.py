import subprocess
import os
from datetime import datetime
import logging

# Define the full format string for commit date
date_format = "%a %b %d %H:%M:%S %Y %z"

def get_git_commits(include_hash: bool, path: str, start_date: str, end_date: str):
    try:    
        # Build the git log command
        git_command = ['git', 'log', '--pretty=format:%H -- %s -- %cd']

        # Add date filtering if start or end date is specified
        if start_date:
            git_command.append(f'--since="{start_date}"')
        if end_date:
            git_command.append(f'--until="{end_date}"')

        logging.info(f"Final git command that will be executed: {" ".join(git_command)}")

        result = subprocess.run(git_command, input="", cwd=path, timeout=15, capture_output=True, text=True, encoding='utf-8')
        # Parse the result into a list of commits
        logging.info(f"Standard output: {result.stdout.splitlines()}")
        commits = []
        for line in result.stdout.splitlines():
            commit_hash, message, date = line.split(' -- ', 2)
            commits.append({
                "hash": commit_hash,
                "message": message,
                "date": date
            })
        final_commits = [generate_bullet_points(commit, include_hash=include_hash) for commit in commits]
        return final_commits if len(final_commits) > 0 else []
    except Exception as e:
        logging.fatal(e)
        return []


# Function to parse the commit date and extract just the time in 12-hour format with AM/PM
def parse_commit_time(date_string):
    try:
        # Parse the full datetime string
        parsed_date = datetime.strptime(date_string, date_format)
        # Extract just the time part in 12-hour format with AM/PM
        return parsed_date.strftime("%I:%M:%S %p")  # Format to 'HH:MM:SS AM/PM'
    except ValueError as e:
        logging.info(e)
        return None

# Function to format the commit into a bullet point
def generate_bullet_points(commit, include_hash=True):
    commit_time = parse_commit_time(commit["date"])
    bullet_point = ""
    if commit_time:
        if include_hash:
            # Bullet point with commit hash
            bullet_point = f"- [{commit['hash'][:7]}] {commit['message']} (committed at {commit_time})"
        else:
            # Bullet point without commit hash
            bullet_point = f"- {commit['message']} (committed at {commit_time})"
    return bullet_point
        

# Function to post work logs to API
def save_work_log(data):
    # Get the current date
    current_date = datetime.now()
    
    # Format the year, full month name, and day
    year = current_date.year
    month_name = current_date.strftime("%B")  # Full month name (e.g., 'August')
    day = current_date.strftime("%d")  # Day of the month with leading zero (e.g., '15')
    short_date = current_date.strftime("%d-%m-%y")  # Short date for filename (e.g., '15-08-25')
    
    # Path to the user's Desktop
    home_directory = os.path.expanduser("~")
    desktop_path = os.path.join(home_directory, "Desktop")
    
    # Path to the work_logs_mcp folder
    logs_folder_path = os.path.join(desktop_path, "work_logs_mcp")
    if not os.path.exists(logs_folder_path):
        os.makedirs(logs_folder_path)
    
    # Path for the year and month folders
    year_folder_path = os.path.join(logs_folder_path, str(year), month_name)
    if not os.path.exists(year_folder_path):
        os.makedirs(year_folder_path)
    
    # Path for the final .md file
    log_file_path = os.path.join(year_folder_path, f"{short_date}.md")

    formatted_data = '\n'
    formatted_data = formatted_data.join(data)

    # Get formatted date
    # Format the year, full month name, and day
    year = current_date.year
    month_name = current_date.strftime("%b")  # Abbreviated month name (e.g., 'Aug')
    day = current_date.strftime("%d")  # Day of the month with leading zero (e.g., '15')
    
    # Create the title
    title = f"Work Log For {day}/{month_name}/{year}"

    formatted_data = '\n--- ' + title + ' ---\n' + formatted_data + '\n--- \n'
    
    # Save the log data to the file
    try:
        with open(log_file_path, 'w', encoding='utf-8') as file:
            file.write(formatted_data)
        logging.info(f"Work log saved successfully at {log_file_path}")
        return log_file_path;
    except Exception as e:
        logging.info(f"Error saving the work log: {e}")