from django.contrib.sessions.backends.db import SessionStore as DbSessionStore
from ebay.models import Basket


class SessionStore(DbSessionStore):
    def cycle_key(self):
        data = self._session
        key = self.session_key
        self.create()
        self._session_cache = data
        if key:
            Basket.objects.filter(session_key=key).update(session_key=self.session_key)
            self.save()
            self.delete(key)
