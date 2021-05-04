class Groups:
    EDITORS = "editors"


editor_permissions = [
    "add_companyrevision",
    "change_company",
    "apply_companyrevision",
    "add_company",
    "add_hashtag",
    "delete_company",
]
groups_permissions = {
    Groups.EDITORS: editor_permissions,
}
