from .base import *
import os
from dotenv import load_dotenv

load_dotenv()

ML_SETTINGS['HF_API_TOKEN'] = os.getenv('HUGGINGFACE_API_TOKEN')

for model in ML_SETTINGS['MODELS'].values():
    model['api_token'] = ML_SETTINGS['HF_API_TOKEN']

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

CORS_ALLOW_ALL_ORIGINS = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
