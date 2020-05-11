Models:
* Users
    User
    Profile

* Community
    Hashtag
    Post
    Company
    Comment
    ModerationFlag

    Like

# Hashtag
  name: Char

# Post
  text: Text (Quill)
  author: Profile
  hashtags: Hashtag

# Company
  name: Char
  slug: Char
  description: Text
  website: Url
  founded_date: Date
  twitter_handle: Char
  crunchbase_id: Char
  employee_count: Choice
  logo: Image
  hashtags: Hashtag

  # Edits
  revision_of: Cls.id
  replaced_by: Cls.id
  approved_by: Profile
  author: Profile

# Comment
  content_type: [ Comment | Company | Post ]
  content: GenericForeignKey
  text: str
  parent: Comment (MPTT)
  author: User
  hashtags: Hashtag
  mentions: User

# Like
  content_type: [ Comment | Company | Post ]
  content: GenericForeignKey
  author: [ User ]


# ModerationFlag
  content_type: [ Comment | Company | Post ]
  content: GenericForeignKey

  flagged: [SPAN, ABUSIVE]
  STATUS: [{PENDING, APPROVED, BLOCKED]
  reviewer: Profile
