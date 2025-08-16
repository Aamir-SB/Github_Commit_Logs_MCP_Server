from core import github_handler
import logging
from mcp.server.fastmcp import FastMCP

# Python print statements are not recommended for MCP protocol development hence using logging package which is recommended
# logging.basicConfig(level=logging.INFO)
# logging.disable(logging.CRITICAL + 1)

# Creating MCP server instance
mcp = FastMCP("weather")

@mcp.tool()
def fill_work_logs(include_hash: bool, path: str, start_date: str, end_date: str) -> str:
    """Fill work logs for today based on github commit messages

    Args:
        include_hash: Whether to include the commit hash in the logs or not this will be python based bool value True or False with first letter capital (eg. True, False) default will be True
        path: User must specify for which project they want to submit the work log otherwise the process will be cancelled
        start_date: User can specify start date for which it wants the github logs. user can specify this date or time in any form but it should be passed in git understandable format for --since flag in git log command. It will default to today's day starting
        end_date: User can specify end date for which it wants the github logs. user can specify this date or time in any form but it should be passed in git understandable format for --until flag in git log command. It will default to today's day ending
    """
    try:
        if path:
            logging.info("Attempting to fetch the work logs for the provided path: " + path)
            work_logs = github_handler.fill_work_log(include_hash=include_hash, path=path, start_date=start_date, end_date=end_date)
            final_response = '\n---\n'.join(work_logs['commits'])
            final_response = final_response + '\n---\nSaved at ' + work_logs['path']
            return '\n----\nUnable to find any work logs for specified time or date' if final_response.strip() == '' or len(work_logs['commits']) <= 0 else final_response
        else:
            return "\n---\nWork logs cannot be saved because no project path was specified"
    except Exception as e:
        return "\n---\nSomething went wrong...Unable to get work logs due to error: " + str(e)


test = {
  'path': 'C:\\Users\\aamir\\OneDrive\\Documents\\Projects\\sample\\react',
  'end_date': 'today 23:59:59',
  'start_date': 'today 00:00:00',
  'include_hash': True
}    

def main():
    # Initialize and run the server
    mcp.run(transport='stdio')
    # result = fill_work_logs(test['include_hash'], test['path'], test['start_date'], test['end_date'])

if __name__ == "__main__":
    main()
