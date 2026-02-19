from pathlib import Path

import pytest

from browniebroke_utils.linkify_github_markdown import (
    add_github_profile_links,
    add_pull_request_links,
    get_link_ranges,
    main,
)


class TestGetLinkRanges:
    def test_no_links(self):
        assert get_link_ranges("no links here") == []

    def test_single_link(self):
        text = "see [link](https://example.com) here"
        ranges = get_link_ranges(text)
        assert ranges == [(4, 31)]

    def test_multiple_links(self):
        text = "[a](url1) and [b](url2)"
        ranges = get_link_ranges(text)
        assert len(ranges) == 2


class TestAddGithubProfileLinks:
    def test_simple_mention(self):
        result = add_github_profile_links("Thanks @octocat")
        assert result == "Thanks [@octocat](https://github.com/octocat)"

    def test_multiple_mentions(self):
        result = add_github_profile_links("@alice and @bob")
        assert result == (
            "[@alice](https://github.com/alice) and [@bob](https://github.com/bob)"
        )

    def test_mention_with_hyphen(self):
        result = add_github_profile_links("@my-user")
        assert result == "[@my-user](https://github.com/my-user)"

    def test_bot_mention(self):
        result = add_github_profile_links("@dependabot[bot]")
        assert result == "[@dependabot[bot]](https://github.com/dependabot[bot])"

    def test_skip_existing_link(self):
        text = "[@octocat](https://github.com/octocat)"
        result = add_github_profile_links(text)
        assert result == text

    def test_skip_decorator(self):
        text = "@versioning_class()"
        result = add_github_profile_links(text)
        assert result == text

    def test_no_mentions(self):
        text = "No mentions here."
        result = add_github_profile_links(text)
        assert result == text


class TestAddPullRequestLinks:
    def test_simple_pr_url(self):
        url = "https://github.com/owner/repo/pull/123"
        result = add_pull_request_links(url)
        assert result == f"[#123]({url})"

    def test_multiple_pr_urls(self):
        content = (
            "https://github.com/owner/repo/pull/1 "
            "and https://github.com/owner/repo/pull/2"
        )
        result = add_pull_request_links(content)
        assert result == (
            "[#1](https://github.com/owner/repo/pull/1)"
            " and "
            "[#2](https://github.com/owner/repo/pull/2)"
        )

    def test_skip_existing_link(self):
        text = "[#123](https://github.com/owner/repo/pull/123)"
        result = add_pull_request_links(text)
        assert result == text

    def test_no_pr_urls(self):
        text = "No PR URLs here."
        result = add_pull_request_links(text)
        assert result == text

    def test_repo_with_hyphens(self):
        url = "https://github.com/my-org/my-repo/pull/42"
        result = add_pull_request_links(url)
        assert result == f"[#42]({url})"


class TestMain:
    def test_processes_file(self, fs):
        input_content = "Fixed by @octocat in https://github.com/owner/repo/pull/99\n"
        fs.create_file("input.md", contents=input_content)

        main(["input.md", "output.md"])

        result = Path("output.md").read_text()
        assert "[@octocat](https://github.com/octocat)" in result
        assert "[#99](https://github.com/owner/repo/pull/99)" in result

    def test_missing_input_file(self, fs):
        with pytest.raises(SystemExit, match="1"):
            main(["missing.md", "output.md"])
