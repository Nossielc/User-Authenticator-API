import env
from libs.api import api

api.run(env.local, env.port, env.debug, env.reloader)