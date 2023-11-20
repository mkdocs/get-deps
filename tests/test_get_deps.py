import contextlib
import os
import tempfile
import textwrap
import unittest

from mkdocs_get_deps import get_deps

_projects_file_path = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "example-projects.yaml"
)


class TestGetDeps(unittest.TestCase):
    @contextlib.contextmanager
    def _assert_logs(self, expected):
        with self.assertLogs("mkdocs.mkdocs_get_deps") as cm:
            yield
        msgs = [f"{r.levelname}:{r.message}" for r in cm.records]
        self.assertRegex("\n".join(msgs), textwrap.dedent(expected).strip("\n"))

    def _test_get_deps(self, yml, expected):
        if yml:
            yml = "site_name: Test\n" + textwrap.dedent(yml)
        with tempfile.TemporaryDirectory() as tempdir:
            mkdocs_yml = os.path.join(tempdir, "mkdocs.yml")
            with open(mkdocs_yml, "w", encoding="utf-8") as f:
                f.write(yml)
            with open(_projects_file_path, encoding="utf-8") as projects_file:
                actual = get_deps(config_file=mkdocs_yml, projects_file=projects_file)
        self.assertEqual(expected, actual)

    def test_empty_config(self):
        expected_logs = "WARNING:The file '.+' doesn't seem to be a mkdocs.yml config file"
        with self._assert_logs(expected_logs):
            self._test_get_deps("", [])

    def test_just_search(self):
        cfg = """
            plugins: [search]
        """
        self._test_get_deps(cfg, ["mkdocs"])

    def test_mkdocs_config(self):
        cfg = """
            site_name: MkDocs
            theme:
              name: mkdocs
              locale: en
            markdown_extensions:
              - toc:
                  permalink: 
              - attr_list
              - def_list
              - tables
              - pymdownx.highlight:
                  use_pygments: false
              - pymdownx.snippets
              - pymdownx.superfences
              - callouts
              - mdx_gh_links:
                  user: mkdocs
                  repo: mkdocs
              - mkdocs-click
            plugins:
              - search
              - redirects:
              - autorefs
              - literate-nav:
                  nav_file: README.md
                  implicit_index: true
              - mkdocstrings:
                  handlers:
                      python:
                          options:
                              docstring_section_style: list
        """
        self._test_get_deps(
            cfg,
            [
                "markdown-callouts",
                "mdx-gh-links",
                "mkdocs",
                "mkdocs-autorefs",
                "mkdocs-click",
                "mkdocs-literate-nav",
                "mkdocs-redirects",
                "mkdocstrings",
                "mkdocstrings-python",
                "pymdown-extensions",
            ],
        )

    def test_dict_keys_and_ignores_env(self):
        cfg = """
            theme:
              name: material
            plugins:
              code-validator:
                enabled: !ENV [LINT, false]
            markdown_extensions:
              pymdownx.emoji:
                emoji_index: !!python/name:materialx.emoji.twemoji
                emoji_generator: !!python/name:materialx.emoji.to_svg
        """
        self._test_get_deps(
            cfg, ["mkdocs", "mkdocs-code-validator", "mkdocs-material", "pymdown-extensions"]
        )

    def test_theme_precedence(self):
        cfg = """
            plugins:
              - tags
            theme: material
        """
        self._test_get_deps(cfg, ["mkdocs", "mkdocs-material"])

        cfg = """
            plugins:
              - material/tags
        """
        self._test_get_deps(cfg, ["mkdocs", "mkdocs-material"])

        cfg = """
            plugins:
              - tags
        """
        self._test_get_deps(cfg, ["mkdocs", "mkdocs-plugin-tags"])

    def test_nonexistent(self):
        cfg = """
            plugins:
              - taglttghhmdu
              - syyisjupkbpo
              - redirects
            theme: qndyakplooyh
            markdown_extensions:
              - saqdhyndpvpa
        """
        expected_logs = """
            WARNING:Theme 'qndyakplooyh' is not provided by any registered project
            WARNING:Plugin 'syyisjupkbpo' is not provided by any registered project
            WARNING:Plugin 'taglttghhmdu' is not provided by any registered project
            WARNING:Extension 'saqdhyndpvpa' is not provided by any registered project
        """
        with self._assert_logs(expected_logs):
            self._test_get_deps(cfg, ["mkdocs", "mkdocs-redirects"])

    def test_git_and_shadowed(self):
        cfg = """
            theme: bootstrap4
            plugins: [blog]
        """
        self._test_get_deps(
            cfg, ["git+https://github.com/andyoakley/mkdocs-blog", "mkdocs", "mkdocs-bootstrap4"]
        )

    def test_multi_theme(self):
        cfg = """
            theme: minty
        """
        self._test_get_deps(cfg, ["mkdocs", "mkdocs-bootswatch"])

    def test_with_locale(self):
        cfg = """
            theme:
                name: mkdocs
                locale: uk
        """
        self._test_get_deps(cfg, ["mkdocs[i18n]"])
