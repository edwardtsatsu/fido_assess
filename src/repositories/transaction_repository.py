from fastapi import Depends
from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import case, desc, func, select
from sqlalchemy.orm import Session, joinedload
from typing_extensions import Annotated

from configs.database import get_db
from src.constants.transaction_type import TransactionType
from src.models.transaction import Transaction
from src.models.user import User
from src.repositories.base_repository import BaseRepository


class TransactionRepository(BaseRepository):
    def __init__(self, db_session: Annotated[Session, Depends(get_db)]):
        super().__init__(model=Transaction, db_session=db_session)

    def find_all(self, query=None):
        db_query = (
            select(self.model)
            .where(self.model.del_status.is_(False))
            .options(joinedload(self.model.user))
            .order_by(desc(self.model.created_at))
        )
        return paginate(
            self.db_session,
            self._parse_query(db_query, query),
            Params(page=query["page"], size=query["size"]),
        )

    def _parse_query(self, db_query, query_param):
        if query_param is None:
            return db_query

        if query_param.get("user_id", None) is not None:
            db_query = db_query.where(self.model.user_id == query_param["user_id"])

        return db_query

    def find_avg_and_total_trans(self, user_id):
        return (
            self.db_session.execute(
                select(
                    func.avg(Transaction.amount),
                    func.sum(
                        case(
                            (
                                Transaction.type == TransactionType.CREDIT,
                                Transaction.amount,
                            ),
                            else_=0,
                        )
                    ),
                    func.sum(
                        case(
                            (
                                Transaction.type == TransactionType.DEBIT,
                                Transaction.amount,
                            ),
                            else_=0,
                        )
                    ),
                )
                .select_from(Transaction)
                .where(Transaction.user_id == user_id)
                .where(Transaction.del_status.is_(False))
            )
        ).fetchone()

    def highest_trans_date(self, user_id):
        return self.db_session.scalar(
            select(
                func.max(Transaction.date),
                func.count(Transaction.id).label("transaction_count"),
            )
            .select_from(Transaction)
            .where(Transaction.user_id == user_id)
            .where(Transaction.del_status.is_(False))
            .group_by(Transaction.date)
            .order_by(desc("transaction_count"))
            .limit(1)
        )
