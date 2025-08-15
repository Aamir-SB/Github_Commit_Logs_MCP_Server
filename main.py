from core import github_handler
import logging

logging.basicConfig(level=logging.INFO)

def main():
    response = github_handler.fill_work_log()


if __name__ == "__main__":
    main()
