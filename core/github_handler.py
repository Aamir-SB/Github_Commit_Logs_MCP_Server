from ..tools import github_tool
import logging

def fill_work_log():
    commits = github_tool.get_git_commits()
    logging.info(str.join(' -- ', commits))