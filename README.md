# manifest-reader
Tool to analyse Android applications manifest.

## Usage

```bash
Usage: manifest-reader [OPTIONS] INPUT

  Tool to read Android manifests. Works with APK files.

Options:
  --android-sdk-version  Retrieve Android SDK version.
  --package-name         Retrieve app's package name.
  --version-name         Retrieve app's version name.
  --xml / --apk          specify input type
  --help                 Show this message and exit.
```

## Install

```bash
$git clone https://github.com/luiscruz/manifest-reader.git
$cd manifest-reader
$pip install .
```
