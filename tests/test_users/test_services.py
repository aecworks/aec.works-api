import pytest

from api.users import services
from api.users.factories import UserFactory


@pytest.mark.django_db
class TestUserServices:
    def test_user_is_editor(self):
        user = UserFactory(groups=["editors"])
        assert services.user_is_editor(user) is True
        user = UserFactory()
        assert services.user_is_editor(user) is False
