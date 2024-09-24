import os

import dotenv

dotenv.load_dotenv(override=True)


GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
GOOGLE_PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")
