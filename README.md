# Default browser redirector

This script on Windows sets itself as a default browser and redirects the link protocol handlers HTTP, HTTPS, and FTP for opening links in different browsers with custom arguments.

## Qualifications

* Are you a power user who uses multiple browsers?
* Do you want to keep browsing sessions separate for different websites?
* Do you want to control which websites open in which browser and in either a new tab or new window?
* Are you tired of manually copying and pasting links into the correct browser?

## Requirements

* [Python 3.10+](https://www.python.org/downloads/)
* [Windows](https://www.microsoft.com/en-us/software-download/windows11/)

## Installation

1) In the "`src`" directory, run "`Install default browser redirector.bat`"
 as administrator.
2) Start > Run (<kbd>Win</kbd> + <kbd>R</kbd>) > `ms-settings:defaultapps`.

   Start > Settings (<kbd>Win</kbd> + <kbd>I</kbd>) > Apps > Default apps.
3) Default browser redirector > Set default file types or link types for HTTP, HTTPS, and FTP > Set default.

## Config file

The script and config file are installed to the "`%AppData%\Default browser redirector`" directory.

[The "`browser_rules.json`" file](/src/browser_rules.json) contains the browsers and the rules in JSON format.

The first browser will be the default browser if no rules apply.

### Browser property

* Each browser provides a `path` to the executable. However, the "clipboard" property does not require it.
* An optional `arguments` property can be a single string or an array of strings.
* If the `clipboard` value is `true`, the URI is copied to the clipboard.

### Rules property

* The `rules` property is an array of strings or objects, containing `text`, `regex`, `arguments`, and `clipboard` properties.

### Regex property

* The `regex` property can be a single string or an object, containing `pattern` and [`flags`](https://docs.python.org/3/library/re.html#flags) properties.

### Examples

[An example "`browser_rules.json`" file](/src/browser_rules.json) is provided and must be edited with your custom values.

* [Opera](https://www.opera.com/download) is the first browser, which is used as the default if no rules apply.
* [Vivaldi](https://vivaldi.com/download/) opens for [github.com](https://github.com), [stackoverflow.com](https://stackoverflow.com), [twitch.tv](https://www.twitch.tv), [ups.com](https://www.ups.com/), and [zillow.com](https://www.zillow.com).
* [Google Chrome](https://www.google.com/chrome/) opens [test.tld](http://test.tld) using the "Profile 12" profile.
* [Mozilla Firefox](https://www.mozilla.org/en-US/firefox/all/#product-desktop-release) opens [firefox.com](http://firefox.com) using the "default" profile and copies the URI to the clipboard.
* [Thorium](https://github.com/Alex313031/thorium/releases) opens [discord.com](https://discord.com) and [Private.tld](http://Private.tld) in a new incognito window and [public.tld](http://public.tld) in a regular tab.
* [Microsoft Edge](https://www.microsoft.com/en-us/edge/download) has no rules and is ignored.
* For the "clipboard" property, [clip.me](https://clip.me) is copied to the clipboard only instead of redirecting to a browser.