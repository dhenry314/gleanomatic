from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import gleanomatic.Utils as Utils

content = Utils.getContent("http://climate-walker.org")

print(content)

