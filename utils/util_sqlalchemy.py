from application.extensions import db


class ModelMixin:

    def update_or_create(self):
        """
        Save a model instance.

        :return: Model instance
        """
        db.session.add(self)
        db.session.commit()

        return self

    def delete(self):
        """
        Delete a model instance.

        :return: db.session.commit()'s result
        """
        db.session.delete(self)
        return db.session.commit()

    @classmethod
    def bulk_update_or_create(cls, items):
        db.session.add_all(items)
        db.session.commit()

    @classmethod
    def bulk_delete(cls, items):
        for item in items:
            db.session.delete(item)
        db.session.commit()

    def __str__(self):
        """
        Create a human readable version of a class instance.

        :return: self
        """
        obj_id = hex(id(self))
        columns = self.__table__.c.keys()

        values = ', '.join("%s=%r" % (n, getattr(self, n)) for n in columns)
        return '<%s %s(%s)>' % (obj_id, self.__class__.__name__, values)
