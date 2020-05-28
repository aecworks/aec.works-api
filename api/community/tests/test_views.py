import pytest
from api.community import factories as f


@pytest.mark.django_db
class TestViews:
    @pytest.mark.parametrize(
        "path,param_factory",
        [
            ["comments/?thread_id={0}", lambda: f.Thread().id],
            ["comments/?parent_id={0}", lambda: f.Comment(thread=f.Thread()).id],
            ["companies/", lambda: f.Company()],
            ["companies/{0}/", lambda: f.Company().slug],
            ["posts/", lambda: f.Post()],
            ["posts/{0}/", lambda: f.Post().slug],
        ],
    )
    def test_get_views_annonymous(
        self, client, django_assert_max_num_queries, path, param_factory
    ):
        if param_factory:
            path = path.format(param_factory())
        url = f"/community/{path}"
        with django_assert_max_num_queries(5):
            resp = client.get(url)
            assert resp.status_code == 200
