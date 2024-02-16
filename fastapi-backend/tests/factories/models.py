import factory
from app.models import CustomerRequest


class CustomerRequestFactory(factory.Factory):
    type: str = factory.Faker("pystr")
    salesforce_id: str = factory.Faker("pystr")
    registration_platform: str = factory.Faker("pystr")
    created_by: str = factory.Faker("pystr")

    class Meta:
        model = CustomerRequest
