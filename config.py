import os
import logging

# Using FLASK_ENV to get the current environment and adjust the configuration.
app_env = os.getenv('FLASK_ENV')

# If FLASK_ENV is not set, flask defaults to production, we want to set to development as default so during local
if app_env is None:
    os.environ['FLASK_ENV'] = 'development'
    app_env = os.getenv('FLASK_ENV')


# Settings applied to specific environments
if app_env == 'production':
    DEBUG = False

elif app_env == 'development':
    DEBUG = True


# required to keep each user session secure and use flasks session variables
# SECRET_KEY = os.environ.get("SECRET_KEY")

# Display configuration that was set in the console
logging.info("Config Env: {}".format(app_env))
