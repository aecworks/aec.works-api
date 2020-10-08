from api.community import factories as f


def test_comments(gql_client):
    thread = f.ThreadFactory()
    comment = f.CommentFactory(thread=thread)
    f.CommentFactory(parent=comment)

    resp = gql_client(
        """
        query {
            commentsByThreadId (threadId: 1) {
                text
                clappers {
                    name
                }
                profile {
                    name
                }
            }
            commentsByParentId (parentId: 1) {
                text
                clappers {
                    name
                }
                profile {
                    name
                }
            }
        }
        """,
    ).json()

    assert "errors" not in resp


def test_companies(gql_client):
    h_a = f.HashtagFactory(slug="a")
    h_b = f.HashtagFactory(slug="b")
    h_c = f.HashtagFactory(slug="c")
    company_a = f.CompanyFactory(name="a", description="abc", twitter="twitter")
    company_b = f.CompanyFactory(name="b", description="abc", twitter="twitter")
    company_c = f.CompanyFactory(name="c", description="abc", twitter="twitter")
    company_a.hashtags.set([h_a, h_c])
    company_b.hashtags.set([h_a, h_b])
    company_c.hashtags.set([h_b, h_c])
    resp = gql_client(
        """
        query {
            companies (hashtagNames: ["a", "b"])  {
                name
                description
                twitter
                articles {
                    url
                }
            }
        }
        """,
    ).json()

    assert "errors" not in resp
    result = resp["data"]["companies"][0]
    assert result["name"] == "b"
    assert "description" in result
    assert "twitter" in result


def test_company_by_slug(gql_client):
    company = f.CompanyFactory(name="xxx", description="abc", twitter="twitter")
    resp = gql_client(
        """
        query {
            companyBySlug (slug: "xxx")  {
                name
                description
                twitter
                articles {
                    url
                }
            }
        }
        """,
    ).json()

    assert "errors" not in resp
    result = resp["data"]["companyBySlug"]
    assert result["name"] == company.name
    assert "description" in result
    assert "twitter" in result


def test_posts(gql_client):
    h_a = f.HashtagFactory(slug="a")
    post_a = f.PostFactory()
    f.PostFactory()
    post_a.hashtags.set([h_a])

    resp = gql_client(
        """
        query {
            posts (hashtagNames: ["a"]) {
                title,
                hashtags {
                    slug
                }
            }
        }
        """,
    ).json()

    assert "errors" not in resp
    assert len(resp["data"]["posts"]) == 1
