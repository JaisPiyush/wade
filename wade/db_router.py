from registry.models import Subscriber

class DatabaseRouter:
    def db_for_read(self, model, **hints) -> str:
        if model == Subscriber:
            return "wade_registry"
        return "default"
    
    def db_for_write(self, model, **hints) -> str:
        if model == Subscriber:
            return "wade_registry"
        return "default"