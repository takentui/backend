import uuid
from datetime import datetime

import factory.fuzzy
from app import db, registry
from tests.utils import AsyncSQLAlchemyFactory


class CustomerFactory(AsyncSQLAlchemyFactory):
    uid = factory.LazyFunction(uuid.uuid4)
    type_ = factory.Faker("pystr", min_chars=10, max_chars=128)
    salesforce_id = factory.Faker("pystr", min_chars=10, max_chars=128)
    registration_platform = factory.Faker("pystr", min_chars=10, max_chars=128)
    created_by = factory.Faker("pystr", min_chars=10, max_chars=128)
    registration_date = factory.LazyFunction(datetime.utcnow)

    class Meta:
        # pylint: disable=unnecessary-lambda-assignment
        model = db.Customer
        async_alchemy_get_or_create = ("uid",)
        async_alchemy_session_factory = lambda: registry.session


class EventFactory(AsyncSQLAlchemyFactory):
    id_ = factory.Faker("pyint")
    topic_name = factory.Faker("pystr", min_chars=10, max_chars=128)
    producer = factory.Faker("pystr", min_chars=10, max_chars=128)
    body = factory.LazyFunction(dict)
    status = factory.fuzzy.FuzzyChoice([1, 2, 3])
    created_at = factory.LazyFunction(datetime.utcnow)

    uid = factory.LazyFunction(uuid.uuid4)
    type_ = factory.Faker("pystr", min_chars=10, max_chars=128)
    salesforce_id = factory.Faker("pystr", min_chars=10, max_chars=128)
    registration_platform = factory.Faker("pystr", min_chars=10, max_chars=128)
    created_by = factory.Faker("pystr", min_chars=10, max_chars=128)
    registration_date = factory.LazyFunction(datetime.utcnow)

    class Meta:
        # pylint: disable=unnecessary-lambda-assignment
        model = db.Event
        async_alchemy_get_or_create = ("uid",)
        async_alchemy_session_factory = lambda: registry.session
