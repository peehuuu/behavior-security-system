# app/extensions.py
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
# app/extensions.py -- add:
from flask_migrate import Migrate
migrate = Migrate()

limiter = Limiter(key_func=get_remote_address)