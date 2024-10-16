import os
from dotenv import load_dotenv


# loads .env file, will not overide already set enviroment variables (will do nothing when testing, building and deploying)
load_dotenv()


DEBUG = os.getenv('DEBUG', 'False') in ['True', 'true']
PORT = os.getenv('PORT', '8080')
POD_NAME = os.getenv('POD_NAME', 'pod_name_not_set')

KEYCLOAK_URL = os.environ["KEYCLOAK_URL"].rstrip()
KEYCLOAK_REALM = os.environ["KEYCLOAK_REALM"].rstrip()
KEYCLOAK_CLIENT_ID = os.environ["KEYCLOAK_CLIENT_ID"].rstrip()
