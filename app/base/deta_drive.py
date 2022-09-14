from deta import Deta

from app.base.config import getProjectKey, settings

deta = Deta(getProjectKey())

drive = deta.Drive(settings.PROJECT_NAME)
