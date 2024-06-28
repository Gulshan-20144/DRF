# routers.py

# user_db/routers.py

class RouterDbRouter:
    """
    A router to control database operations on models in the user_db app.
    """ 
    app_router=['RouterApp','auth','contenttype']

    def db_for_read(self, model, **hints):
        """
        Attempts to read from user_db database.
        """
        if model._meta.app_label in self.app_router:
            return 'user_db'
        return "default"

    def db_for_write(self, model, **hints):
        """
        Attempts to write to user_db database.
        """
        if model._meta.app_label in self.app_router:
            return 'user_db'
        return "default"

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if both models are in user_db app.
        """
        if (
            obj1._meta.app_label in self.app_router or
            obj2._meta.app_label in self.app_router
        ):
            return True
        return "default"

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the user_db app only appears in the 'user_db' database.
        """
        if app_label in self.app_router:
            return db == 'user_db'
        return "default"
