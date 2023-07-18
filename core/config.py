import os
from dotenv import load_dotenv

load_dotenv()

# DATABASE Config
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASS')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')

db_url = f"postgres://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

# Other Config
refresh_rate = db_name = os.getenv('REFRESH_RATE')
