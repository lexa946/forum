from app.dao.base import BaseDAO
from app.threads.models import Thread


class ThreadDAO(BaseDAO):
    model = Thread


