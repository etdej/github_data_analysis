EVENT_EXTRACTION_DEF_LS = list()

_COMMON_SPECS = [
    ("id", ),
    ("created_at", ),
    ("repo", "id"),
    ("repo", "name"),
    ("actor", "id"),
    ("actor", "login"),
    ("public", ),
]

EVENT_EXTRACTION_DEF_LS.append({
    "type": "PullRequestEvent",
    "spec_ls": _COMMON_SPECS + [
        ("payload", "action"),
        ("payload", "number"),
        ("payload", "pull_request", "base", "repo", "id"),
        ("payload", "pull_request", "base", "repo", "name"),
        ("payload", "pull_request", "base", "user", "id"),
        ("payload", "pull_request", "base", "user", "login"),
        ("payload", "pull_request", "base", "ref"),
        ("payload", "pull_request", "head", "repo", "id"),
        ("payload", "pull_request", "head", "repo", "name"),
        ("payload", "pull_request", "head", "user", "id"),
        ("payload", "pull_request", "head", "user", "login"),
        ("payload", "pull_request", "head", "ref"),
        ("payload", "pull_request", "created_at"),
        ("payload", "pull_request", "closed_at"),
        ("payload", "pull_request", "comments"),
        ("payload", "pull_request", "review_comments"),
        ("payload", "pull_request", "commits"),
        ("payload", "pull_request", "additions"),
        ("payload", "pull_request", "deletions"),
        ("payload", "pull_request", "changed_files"),
        ("payload", "pull_request", "merged_at"),
        ("payload", "pull_request", "merged_by"),
        ("payload", "pull_request", "user", "id"),
        ("payload", "pull_request", "user", "login"),
    ],
    "repo_loc_ls": [
        ("repo", ),
        ("payload", "pull_request", "base", "repo"),
        ("payload", "pull_request", "head", "repo"),
    ],
})

"""
EVENT_EXTRACTION_DEF_LS.append({
    "type": "PullRequestReviewEvent",
    "spec_ls": _COMMON_SPECS + [
        ("payload", "action"),
        ("payload", "review", "id"),
        ("payload", "review", "user", "id"),
        ("payload", "review", "user", "login"),
        ("payload", "review", "user", "submitted_at"),
        ("payload", "review", "user", "state"),
        ("payload", "pull_request", "base", "repo", "id"),
        ("payload", "pull_request", "base", "repo", "name"),
        ("payload", "pull_request", "base", "user", "id"),
        ("payload", "pull_request", "base", "user", "login"),
        ("payload", "pull_request", "base", "ref"),
        ("payload", "pull_request", "head", "repo", "id"),
        ("payload", "pull_request", "head", "repo", "name"),
        ("payload", "pull_request", "head", "user", "id"),
        ("payload", "pull_request", "head", "user", "login"),
        ("payload", "pull_request", "head", "ref"),
        ("payload", "pull_request", "created_at"),
        ("payload", "pull_request", "closed_at"),
        ("payload", "pull_request", "comments"),
        ("payload", "pull_request", "review_comments"),
        ("payload", "pull_request", "commits"),

        ("payload", "pull_request", "deletions"),
        ("payload", "pull_request", "changed_files"),
        ("payload", "pull_request", "merged_at"),
        ("payload", "pull_request", "merged_by"),
        ("payload", "pull_request", "user", "id"),
        ("payload", "pull_request", "user", "login"),
    ],
    "repo_loc_ls": [
        ("repo", ),
        ("payload", "pull_request", "base", "repo"),
        ("payload", "pull_request", "head", "repo"),
    ],
})
"""

EVENT_EXTRACTION_DEF_LS.append({
    "type": "PullRequestReviewCommentEvent",
    "spec_ls": _COMMON_SPECS + [
        ("payload", "action"),
        ("payload", "comment", "id"),
        ("payload", "comment", "user", "id"),
        ("payload", "comment", "user", "login"),
        ("payload", "comment", "created_at"),
        ("payload", "comment", "updated_at"),
        ("payload", "comment", "commit_id"),
        ("payload", "comment", "original_commit_id"),
        ("payload", "pull_request", "base", "repo", "id"),
        ("payload", "pull_request", "base", "repo", "name"),
        ("payload", "pull_request", "base", "user", "id"),
        ("payload", "pull_request", "base", "user", "login"),
        ("payload", "pull_request", "base", "ref"),
        ("payload", "pull_request", "head", "repo", "id"),
        ("payload", "pull_request", "head", "repo", "name"),
        ("payload", "pull_request", "head", "user", "id"),
        ("payload", "pull_request", "head", "user", "login"),
        ("payload", "pull_request", "head", "ref"),
        ("payload", "pull_request", "created_at"),
        ("payload", "pull_request", "closed_at"),
        ("payload", "pull_request", "merged_at"),
        ("payload", "pull_request", "user", "id"),
        ("payload", "pull_request", "user", "login"),
    ],
    "repo_loc_ls": [
        ("repo", ),
        ("payload", "pull_request", "base", "repo"),
        ("payload", "pull_request", "head", "repo"),
    ],
})

EVENT_EXTRACTION_DEF_LS.append({
    "type": "PushEvent",
    "spec_ls": _COMMON_SPECS + [
        ("payload", "ref"),
        ("payload", "size"),
        ("payload", "distinct_size"),
    ],
    "repo_loc_ls": [
        ("repo", ),
    ],
})

EVENT_EXTRACTION_DEF_LS.append({
    "type": "ForkEvent",
    "spec_ls": _COMMON_SPECS + [
        ("payload", "forkee", "id"),
        ("payload", "forkee", "name"),
    ],
    "repo_loc_ls": [
        ("repo", ),
    ],
})

EVENT_EXTRACTION_DEF_LS.append({
    "type": "MemberEvent",
    "spec_ls": _COMMON_SPECS + [
        ("payload", "action"),
        ("payload", "member", "id"),
        ("payload", "member", "login"),
    ],
    "repo_loc_ls": [
        ("repo", ),
    ],
})

EVENT_EXTRACTION_DEF_LS.append({
    "type": "IssuesEvent",
    "spec_ls": _COMMON_SPECS + [
        ("payload", "action"),
        ("payload", "issue", "user", "id"),
        ("payload", "issue", "user", "login"),
        ("payload", "issue", "id"),
        ("payload", "issue", "state"),
        ("payload", "issue", "locked"),
        ("payload", "issue", "created_at"),
        ("payload", "issue", "updated_at"),
        ("payload", "issue", "closed_at"),
        ("payload", "issue", "comments"),
    ],
    "repo_loc_ls": [
        ("repo", ),
    ],
})

EVENT_EXTRACTION_DEF_LS.append({
    "type": "IssueCommentEvent",
    "spec_ls": _COMMON_SPECS + [
        ("payload", "action"),
        ("payload", "issue", "user", "id"),
        ("payload", "issue", "user", "login"),
        ("payload", "issue", "id"),
        ("payload", "issue", "state"),
        ("payload", "issue", "locked"),
        ("payload", "issue", "created_at"),
        ("payload", "issue", "updated_at"),
        ("payload", "issue", "closed_at"),
        ("payload", "issue", "comments"),
        ("payload", "comment", "user", "id"),
        ("payload", "comment", "user", "login"),
        ("payload", "comment", "created_at"),
        ("payload", "comment", "updated_at"),
    ],
    "repo_loc_ls": [
        ("repo", ),
    ],
})

"""
EVENT_EXTRACTION_DEF_LS.append({
    "type": "LabelEvent",
    "spec_ls": _COMMON_SPECS + [
        ("repo", "id"),
        ("repo", "name"),
        ("actor", "id"),
        ("actor", "login"),
        ("payload", "action"),
        ("payload", "label", "name"),
    ],
    "repo_loc_ls": [
        ("repo", ),
    ],
})
"""

EVENT_EXTRACTION_DEF_LS.append({
    "type": "WatchEvent",
    "spec_ls": _COMMON_SPECS + [
        ("payload", "action"),
    ],
    "repo_loc_ls": [
        ("repo", ),
    ],
})

EVENT_EXTRACTION_DEF_LS.append({
    "type": "CreateEvent",
    "spec_ls": _COMMON_SPECS + [
        ("payload", "ref_type"),
        ("payload", "ref"),
        ("payload", "master_branch"),
        ("payload", "pusher_type"),
    ],
    "repo_loc_ls": [
        ("repo", ),
    ],
})


# ======== #

REPO_SPEC_LS = [
    ("owner", "id"),
    ("owner", "login"),
    ("name", ),
    ("id", ),
    ("private", ),
    ("fork", ),
    ("homepage", ),
    ("size", ),
    ("stargazers_count",),
    ("watchers_count",),
    ("language",),
    ("has_issues", ),
    ("has_downloads", ),
    ("has_wiki", ),
    ("has_pages", ),
    ("forks_count", ),
    ("open_issues_count", ),
    ("forks", ),
    ("open_issues", ),
    ("watchers", ),
    ("default_branch", ),
    # Also collect:
    # - id
    # - created_at
]
