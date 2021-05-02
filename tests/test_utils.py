from api.common.utils import increment_slug


def test_slug_generation():
    assert increment_slug("my-company") == "my-company-2"
    assert increment_slug("my-company-2") == "my-company-3"
    assert increment_slug("my-company-9") == "my-company-10"
    assert increment_slug("a") == "a-2"
