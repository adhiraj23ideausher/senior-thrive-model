from dotenv import load_dotenv, dotenv_values
load_dotenv()
import os

print(os.getenv('NAME'))