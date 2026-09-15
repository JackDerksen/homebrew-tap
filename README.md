# Jack's Homebrew tap

Install [Redox](https://github.com/JackDerksen/redox) on macOS or Linux:

```sh
brew install jackderksen/tap/redox
```

Update it with:

```sh
brew update
brew upgrade redox
```

Homebrew builds Redox from its pinned release source and installs the required build
tools. The formula checks the source archive's SHA-256 and uses Cargo's lockfile.

The **Update Redox** workflow checks GitHub's latest stable release hourly. When a
new version appears, it updates the source URL and checksum, builds and tests the
formula on macOS and Linux, then commits the tested update. It can also be run
manually from the Actions tab. Only the tap's built-in GitHub token is needed.

Formula changes and pull requests run the same installation tests. The first
packaged release is v0.8.1, so its test checks command-line argument validation;
that release does not support `redox --version` yet.
