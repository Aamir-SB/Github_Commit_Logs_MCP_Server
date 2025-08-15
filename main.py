from core import github_handler
import logging

def main():
    response = github_handler.fill_work_log()
    logging.info("Filled work logs successfully for today")


if __name__ == "__main__":
    main()
