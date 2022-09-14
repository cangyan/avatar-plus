from deta import Deta

from app.base.config import getProjectKey, settings

deta = Deta(getProjectKey())

db = deta.Base(settings.PROJECT_NAME)
