import pytest
from django.core.exceptions import PermissionDenied
from api.users.factories import ProfileFactory
from api.community import factories, services


@pytest.mark.django_db
class TestServices:
    def test_create_post(self):
        profile = ProfileFactory()
        title = "Hello Friends"
        body = """<p>Image</p><p><img src=\"data:image/png;base64,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\"></p>"""
        hashtag_names = ["webapp", "bagels"]
        post = services.create_post(
            profile=profile, title=title, body=body, hashtag_names=hashtag_names
        )
        assert post.title == title
        assert post.hashtags.filter(slug="bagels").exists()
        # Cover image was created and is also stored in post.images
        assert post.images.filter(id=post.cover.id).exists()

    def test_excract_cover(self):
        profile = ProfileFactory()
        test_post_body = """<p>Image</p><p><img src=\"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAwAAAAGCAYAAAD37n+BAAAMZGlDQ1BJQ0MgUHJvZmlsZQAASImVVwdck0cbv3dkkrACEZAR9hJFZgAZIawIAjIFUQlJIGHEmBBUXIiWKli3iOKoaFVAwToAqQMR6yyK2zqKA5VKLVZxofJdSEBrv/H7nt/v3vu/zz33f0bu8t4BoNPJl8lyUV0A8qT58rjwYNaklFQW6REgAhRogzHAmC9QyDixsVEAylD/d3l9HSCq/oqLiuuf4/9V9IUihQAAJA3iDKFCkAdxCwB4sUAmzweAGAL11jPzZSoshthADgOEeK4KZ6nxShXOUOMdgzYJcVyImwAg0/h8eRYA2m1QzyoQZEEe7UcQu0qFEikAOgYQBwjEfCHECRCPysubrsJFEDtAexnEuyFmZ3zBmfU3/oxhfj4/axir8xoUcohEIcvlz/4/S/O/JS9XOeTDDjaaWB4Rp8of1vBmzvRIFaZB3CPNiI5R1RritxKhuu4AoFSxMiJRbY+aChRcWD/AhNhVyA+JhNgU4jBpbnSURp+RKQnjQQxXCzpLks9L0MxdIlKExms4N8mnx8UM4Uw5l6OZW8eXD/pV2bcpcxI5Gv6bYhFviP9VoTghGWIqABi1QJIUDbE2xAaKnPhItQ1mVSjmRg/ZyJVxqvhtIGaLpOHBan4sLVMeFqexl+UphvLFSsQSXrQGV+SLEyLU9cFqBPzB+I0gbhBJOYlDPCLFpKihXISikFB17li7SJqoyRe7J8sPjtPM7ZXlxmrscbIoN1ylt4LYRFEQr5mLj8uHi1PNj0fJ8mMT1HHi6dn88bHqePACEAW4IASwgBK2DDAdZANJe09jD3xTj4QBPpCDLCACLhrN0IzkwREpfMaDQvAHRCKgGJ4XPDgqAgVQ/3FYq366gMzB0YLBGTngMcR5IBLkwnfl4CzpsLck8AhqJP/wLoCx5sKmGvunjgM1URqNcoiXpTNkSQwlhhAjiGFER9wED8D98Cj4DILNDWfjPkPRfrYnPCZ0EB4QrhE6CbemSYrlX8UyAXRC/jBNxhlfZozbQU5PPBj3h+yQGWfiJsAF94B+OHgg9OwJtVxN3KrcWf8mz+EMvqi5xo7iSkEpIyhBFIevZ2o7aXsOs6gq+mV91LFmDFeVOzzytX/uF3UWwj7ya0tsCXYAO42dwM5iR7BGwMKOY03YBeyoCg+voUeDa2jIW9xgPDmQR/IPf3yNT1UlFa61rt2uHzRjIF80K1+1wbjTZbPlkixxPosDvwIiFk8qGD2K5ebq5gqA6pui/pt6yRz8ViDMc591xXcB8E8ZGBg48lkXBffpwadwm/d81tnXAkA/BsCZbwRKeYFah6seBPhvoAN3lDEwB9bAAWbkBryAHwgCoWA8iAEJIAVMhXUWw/UsBzPBXLAQlIAysBKsAxvBVrAd7AZ7wX7QCI6AE+BncB5cAtfAbbh+usAz0Ateg34EQUgIHWEgxogFYos4I24IGwlAQpEoJA5JQdKRLESKKJG5yCKkDFmNbES2IdXIj8hh5ARyFulAbiH3kW7kL+Q9iqE01AA1Q+3QMSgb5aCRaAI6Bc1CZ6CF6GJ0OVqBVqF70Ab0BHoevYZ2os/QPgxgWhgTs8RcMDbGxWKwVCwTk2PzsVKsHKvC6rBm+EtfwTqxHuwdTsQZOAt3gWs4Ak/EBfgMfD6+DN+I78Yb8Db8Cn4f78U/EegEU4IzwZfAI0wiZBFmEkoI5YSdhEOEU3A3dRFeE4lEJtGe6A13YwoxmziHuIy4mVhPbCF2EB8S+0gkkjHJmeRPiiHxSfmkEtIG0h7ScdJlUhfpLVmLbEF2I4eRU8lScjG5nFxDPka+TH5C7qfoUmwpvpQYipAym7KCsoPSTLlI6aL0U/Wo9lR/agI1m7qQWkGto56i3qG+1NLSstLy0ZqoJdEq0qrQ2qd1Ruu+1juaPs2JxqWl0ZS05bRdtBbaLdpLOp1uRw+ip9Lz6cvp1fST9Hv0t9oM7dHaPG2h9gLtSu0G7cvaz3UoOrY6HJ2pOoU65ToHdC7q9OhSdO10ubp83fm6lbqHdW/o9ukx9Mbqxejl6S3Tq9E7q/dUn6Rvpx+qL9RfrL9d/6T+QwbGsGZwGQLGIsYOxilGlwHRwN6AZ5BtUGaw16DdoNdQ39DDMMlwlmGl4VHDTibGtGPymLnMFcz9zOvM9yPMRnBGiEYsHVE34vKIN0YjjYKMREalRvVG14zeG7OMQ41zjFcZNxrfNcFNnEwmmsw02WJyyqRnpMFIv5GCkaUj94/81RQ1dTKNM51jut30gmmfmblZuJnMbIPZSbMec6Z5kHm2+VrzY+bdFgyLAAuJxVqL4xa/swxZHFYuq4LVxuq1NLWMsFRabrNst+y3srdKtCq2qre6a021ZltnWq+1brXutbGwmWAz16bW5ldbii3bVmy73va07Rs7e7tku2/tGu2e2hvZ8+wL7Wvt7zjQHQIdZjhUOVx1JDqyHXMcNzteckKdPJ3ETpVOF51RZy9nifNm545RhFE+o6SjqkbdcKG5cFwKXGpd7o9mjo4aXTy6cfTzMTZjUsesGnN6zCdXT9dc1x2ut8fqjx0/tnhs89i/3JzcBG6Vblfd6e5h7gvcm9xfeDh7iDy2eNz0ZHhO8PzWs9Xzo5e3l9yrzqvb28Y73XuT9w22ATuWvYx9xofgE+yzwOeIzztfL9983/2+f/q5+OX41fg9HWc/TjRux7iH/lb+fP9t/p0BrID0gO8DOgMtA/mBVYEPgqyDhEE7g55wHDnZnD2c58GuwfLgQ8FvuL7cedyWECwkPKQ0pD1UPzQxdGPovTCrsKyw2rDecM/wOeEtEYSIyIhVETd4ZjwBr5rXO957/LzxbZG0yPjIjZEPopyi5FHNE9AJ4yesmXAn2jZaGt0YA2J4MWti7sbax86I/WkicWLsxMqJj+PGxs2NOx3PiJ8WXxP/OiE4YUXC7USHRGVia5JOUlpSddKb5JDk1cmdk8ZMmjfpfIpJiiSlKZWUmpS6M7VvcujkdZO70jzTStKuT7GfMmvK2akmU3OnHp2mM40/7UA6IT05vSb9Az+GX8Xvy+BlbMroFXAF6wXPhEHCtcJukb9otehJpn/m6synWf5Za7K6xYHicnGPhCvZKHmRHZG9NftNTkzOrpyB3OTc+jxyXnreYam+NEfaNt18+qzpHTJnWYmsc4bvjHUzeuWR8p0KRDFF0ZRvAA/vF5QOym+U9wsCCioL3s5Mmnlglt4s6awLs51mL539pDCs8Ic5+BzBnNa5lnMXzr0/jzNv23xkfsb81gXWCxYv6CoKL9q9kLowZ+Evxa7Fq4tfLUpe1LzYbHHR4offhH9TW6JdIi+58a3ft1uX4EskS9qXui/dsPRTqbD0XJlrWXnZh2WCZee+G/tdxXcDyzOXt6/wWrFlJXGldOX1VYGrdq/WW124+uGaCWsa1rLWlq59tW7aurPlHuVb11PXK9d3VkRVNG2w2bByw4eN4o3XKoMr6zeZblq66c1m4ebLW4K21G0121q29f33ku9vbgvf1lBlV1W+nbi9YPvjHUk7Tv/A/qF6p8nOsp0fd0l3de6O291W7V1dXWNas6IWrVXWdu9J23Npb8jepjqXum31zPqyfWCfct/vP6b/eH1/5P7WA+wDdQdtD246xDhU2oA0zG7obRQ3djalNHUcHn+4tdmv+dBPo3/adcTySOVRw6MrjlGPLT42cLzweF+LrKXnRNaJh63TWm+fnHTyatvEtvZTkafO/Bz288nTnNPHz/ifOXLW9+zhc+xzjee9zjdc8Lxw6BfPXw61e7U3XPS+2HTJ51Jzx7iOY5cDL5+4EnLl56u8q+evRV/ruJ54/eaNtBudN4U3n97KvfXi14Jf+28X3SHcKb2re7f8num9qt8cf6vv9Oo8ej/k/oUH8Q9uPxQ8fPZI8ehD1+LH9MflTyyeVD91e3qkO6z70u+Tf+96JnvW31Pyh94fm547PD/4Z9CfF3on9Xa9kL8Y+GvZS+OXu155vGrti+279zrvdf+b0rfGb3e/Y787/T75/ZP+mR9IHyo+On5s/hT56c5A3sCAjC/nDx4FMNjQzEwA/toFzwkpADAuwfPDZPWdb1AQ9T11EIH/hNX3wkHxAqAOdqrjOrcFgH2w2RVBbviuOqonBAHU3X24aUSR6e6m5qLBGw/h7cDASzMASM0AfJQPDPRvHhj4CO+o2C0AWmao75oqIcK7wfdBKnTNSFgEvhL1PfSLHL/ugSoCD/B1/y96O4mN7DpJkAAAAIplWElmTU0AKgAAAAgABAEaAAUAAAABAAAAPgEbAAUAAAABAAAARgEoAAMAAAABAAIAAIdpAAQAAAABAAAATgAAAAAAAACQAAAAAQAAAJAAAAABAAOShgAHAAAAEgAAAHigAgAEAAAAAQAAAAygAwAEAAAAAQAAAAYAAAAAQVNDSUkAAABTY3JlZW5zaG90cntYbwAAAAlwSFlzAAAWJQAAFiUBSVIk8AAAAdNpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IlhNUCBDb3JlIDUuNC4wIj4KICAgPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICAgICAgPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIKICAgICAgICAgICAgeG1sbnM6ZXhpZj0iaHR0cDovL25zLmFkb2JlLmNvbS9leGlmLzEuMC8iPgogICAgICAgICA8ZXhpZjpQaXhlbFhEaW1lbnNpb24+MTI8L2V4aWY6UGl4ZWxYRGltZW5zaW9uPgogICAgICAgICA8ZXhpZjpVc2VyQ29tbWVudD5TY3JlZW5zaG90PC9leGlmOlVzZXJDb21tZW50PgogICAgICAgICA8ZXhpZjpQaXhlbFlEaW1lbnNpb24+NjwvZXhpZjpQaXhlbFlEaW1lbnNpb24+CiAgICAgIDwvcmRmOkRlc2NyaXB0aW9uPgogICA8L3JkZjpSREY+CjwveDp4bXBtZXRhPgpomYYWAAAAHGlET1QAAAACAAAAAAAAAAMAAAAoAAAAAwAAAAMAAABf7W7m4QAAACtJREFUKBVivJ+W/5+BBMBIrAZGBkaG/wz/GAhr+A9UBIQM/1kY/jH/YAAAAAD//8+H4R0AAAA9SURBVH2NwRGAMBACl0yMVurXki3EM0gDBp4soPu8zK+EmEmDeOPtD1oVTIsndmF1vI91geDKuqm8NGocfCg6J0aY6R75AAAAAElFTkSuQmCC\"></p>"""
        body, imgs = services.extract_image_assets(test_post_body, profile)
        assert len(imgs) == 1
        assert imgs[0].created_by == profile
        assert imgs[0].file.url in body

    def test_post_clap(self):
        profile = ProfileFactory()
        post = factories.PostFactory()
        assert post.clappers.count() == 0
        rv = services.post_clap(post=post, profile=profile)
        assert rv == 1
        rv2 = services.post_clap(post=post, profile=profile)
        assert rv2 == 1
        assert post.clappers.count() == 1

    def test_companyClap(self):
        profile = ProfileFactory()
        company = factories.CompanyFactory()
        assert company.clappers.count() == 0
        rv = services.company_clap(company=company, profile=profile)
        assert rv == 1
        rv2 = services.company_clap(company=company, profile=profile)
        assert rv2 == 1
        assert company.clappers.count() == 1

    def test_comment_clap(self):
        thread = factories.ThreadFactory()
        comment = factories.CommentFactory(thread=thread)
        profile = ProfileFactory()
        assert comment.clappers.count() == 0
        rv = services.comment_clap(comment=comment, profile=profile)
        assert rv == 1
        rv2 = services.comment_clap(comment=comment, profile=profile)
        assert rv2 == 1
        assert comment.clappers.count() == 1

    def test_edit_post(self):
        post = factories.PostFactory()
        updated_post = services.update_post(
            profile=post.profile, slug=post.slug, title="x", body="x", hashtag_names=[]
        )
        assert updated_post.title == "x"

    def test_edit_permissions(self):
        profile = ProfileFactory()
        post = factories.PostFactory()
        with pytest.raises(PermissionDenied):
            services.update_post(
                profile=profile, slug=post.slug, title="x", body="x", hashtag_names=[]
            )
        profile.user.is_staff = True
        profile.save()
        updated_post = services.update_post(
            profile=profile, slug=post.slug, title="x", body="x", hashtag_names=[]
        )
        assert updated_post.title == "x"

    def test_create_revision(self):
        profile = ProfileFactory()
        company = factories.CompanyFactory()
        revision = services.create_revision(
            company=company, profile=profile, validated_data={"name": "x"}
        )
        assert revision.company == company
        assert revision.name == "x"

    def test_apply_revision(self):
        h_a = factories.HashtagFactory(slug="a")
        h_b = factories.HashtagFactory(slug="b")
        h_c = factories.HashtagFactory(slug="c")

        profile = ProfileFactory()
        hashtags = [h_a, h_b]
        company = factories.CompanyFactory()
        company.hashtags.set(hashtags)

        revision = factories.CompanyRevisionFactory(company=company)
        new_hahstags = [h_a, h_c]
        revision.hashtags.set(new_hahstags)

        services.apply_revision(revision=revision, profile=profile)

        assert company.last_revision == revision
        assert revision.company == company
        assert revision.approved_by == profile
        assert revision.applied is True
        assert set([h.slug for h in company.hashtags.all()]) == set(["a", "c"])

    def test_create_comment(self):
        profile = ProfileFactory()
        text = "xxx"
        thread = factories.ThreadFactory()
        assert thread.size == 0

        comment = services.create_comment(profile=profile, text=text, thread=thread)
        assert thread.size == 1
        assert comment.text == text
        assert comment.profile == profile

        services.create_comment(
            profile=profile, text=text, thread=thread, parent=comment
        )
        assert comment.reply_count == 1
        assert thread.size == 2
