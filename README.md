# mkdocs-get-deps

**An extra command for [MkDocs][] that infers required PyPI packages from `plugins` in mkdocs.yml.**

[![PyPI](https://img.shields.io/pypi/v/mkdocs-get-deps)](https://pypi.org/project/mkdocs-get-deps/)
[![GitHub](https://img.shields.io/github/license/mkdocs/get-deps)](https://github.com/mkdocs/get-deps/blob/master/LICENSE.md)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/mkdocs/get-deps/ci.yml.svg)](https://github.com/mkdocs/get-deps/actions?query=event%3Apush+branch%3Amaster)

<table>
<tr><td>Installation:</td><td>Alternatively through MkDocs itself:</td></tr>
<tr><td>

```bash
pip install mkdocs-get-deps
```

</td><td>

```bash
pip install mkdocs
```

</td>
</tr></table>


This command guesses the Python dependencies that a MkDocs site requires in order to build. It simply prints the PyPI packages that need to be installed. In the terminal it can be combined directly with a `pip install` command, as per the last example below:

<table>
<tr><td>Usage:</td><td>Alternatively through MkDocs itself:</td></tr>
<tr><td>

```bash
# Print dependencies of the current project
mkdocs-get-deps
# Save them into a file
mkdocs-get-deps > requirements.txt
# Install dependencies on the fly
pip install $(mkdocs-get-deps)
```

</td><td>

```bash

mkdocs get-deps

mkdocs get-deps > requirements.txt
pip install -r requirements.txt

pip install $(mkdocs get-deps)
```

</td>
</tr></table>

The idea is that right after running this command, you can directly follow it up with `mkdocs build` and it will almost always "just work", without needing to think which dependencies to install.

The way it works is by scanning [`mkdocs.yml`] for `themes:`, `plugins:`, `markdown_extensions:` items and doing a reverse lookup based on a large list of known projects (catalog, see below).

Of course, you're encouraged to use a "virtualenv" with such a command. Also note that for environments that require stability (for example CI) directly installing deps in this way is not a very reliable approach as it precludes dependency pinning.

The command allows overriding which config file is used (instead of `mkdocs.yml` in the current directory) as well as which catalog of projects is used (instead of downloading it from the default location). See [`mkdocs get-deps --help`](https://www.mkdocs.org/user-guide/cli/#mkdocs-get-deps).

## MkDocs' official catalog of plugins

Check out <https://github.com/mkdocs/catalog> and add all your general-purpose plugins, themes and extensions there, so that they can be looked up through `mkdocs get-deps`.

[MkDocs]: https://www.mkdocs.org/
[`mkdocs.yml`]: https://www.mkdocs.org/user-guide/configuration/
