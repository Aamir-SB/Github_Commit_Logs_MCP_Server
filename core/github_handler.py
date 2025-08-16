from tools import github_tool
import logging

def fill_work_log(include_hash: bool, path: str, start_date: str, end_date: str):
    logging.info(f"Fetching the github commit logs for the specified parameters: Hash: {include_hash}, Path: {path}, start date: {start_date}, end date: {end_date}")
    commits = github_tool.get_git_commits(include_hash=include_hash, path=path, start_date=start_date, end_date=end_date)
    logging.info(f"Github commits fetched successfully. Trying to generate a file on desktop with provided commits: {commits}, Total number of commits found: {len(commits)}")
    logging_path = github_tool.save_work_log(commits)
    logging.info(f"File saved successfully at {logging_path}, Total number of commits saved: {len(commits)}")
    logging.info("Returning the commits to AI for better description and analaysis by user")    
    return {
        "commits": commits,
        "path": logging_path
    }