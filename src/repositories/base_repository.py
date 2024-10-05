from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import desc, select, update


class BaseRepository:
    def __init__(self, model, db_session):
        self.model = model
        self.db_session = db_session

    def find_all(self, query=None):
        db_query = (
            select(self.model)
            .where(self.model.del_status.is_(False))
            .order_by(desc(self.model.created_at))
        )
        return paginate(self.db_session, db_query)

    def find(self, id):
        return self.db_session.scalars(
            select(self.model)
            .where(self.model.del_status.is_(False))
            .where(self.model.id == id)
        ).first()

    def update(self, id, data):
        self.db_session.execute(
            update(self.model)
            .where(self.model.del_status.is_(False))
            .where(self.model.id == id)
            .values(**data)
        )
        self.db_session.commit()
        return self.find(id)

    def store(self, data):
        resource = self.model(**data)
        self.db_session.add(resource)
        self.db_session.commit()
        self.db_session.refresh(resource)
        return resource

    def delete(self, id):
        self.db_session.execute(
            update(self.model)
            .where(self.model.del_status.is_(False))
            .where(self.model.id == id)
            .values(del_status=True)
        )
        self.db_session.commit()
