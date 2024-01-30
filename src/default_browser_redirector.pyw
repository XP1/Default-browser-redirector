#!/usr/bin/env pythonw
"""
Copyright 2024 XP1

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
import re
import sys
import json
import subprocess
import traceback
from typing import Any, Pattern


def write_to_clipboard(text: str):
    clip = subprocess.Popen("clip", stdin=subprocess.PIPE, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
    clip.communicate(input=text)


def handle_exception(exception):
    exception_text = "".join(traceback.format_exception(exception))
    print("Exception:")
    print(exception_text)
    print()
    write_to_clipboard(exception_text)


def change_to_file_directory(file_path: str) -> None:
    directory_path = os.path.dirname(file_path)
    os.chdir(directory_path)


def fetch_json_file(path: str) -> Any:
    with open(path, encoding="utf-8") as file:
        data = json.load(file)
        return data


RuleDataType = str | dict | None


class BrowserRules():
    def __init__(self) -> None:
        self.browser_rules: dict = fetch_json_file("browser_rules.json")

    def get_first_browser(self) -> dict:
        return next(iter(self.browser_rules.values()))

    @staticmethod
    def parse_regex(regex: str | dict) -> Pattern[str | None]:
        pattern = None
        flags = 0
        if isinstance(regex, str):
            pattern = regex
        elif isinstance(regex, dict):
            if "pattern" in regex:
                pattern = regex["pattern"]
            else:
                raise TypeError(f"Regex \"{regex}\" must have a pattern.")

            if "flags" in regex:
                regex_flags = regex["flags"]
                if isinstance(regex_flags, (str, int)):
                    regex_flags = [regex_flags]
                elif not isinstance(regex_flags, list):
                    raise TypeError(f"Flags \"{regex_flags}\" must be a list, string, or int.")

                f = 0
                for regex_flag in regex_flags:
                    if isinstance(regex_flag, str):
                        f += getattr(re, regex_flag)
                    elif isinstance(regex_flag, int):
                        f += regex_flag
                    else:
                        raise TypeError(f"Flag \"{regex_flag}\" must be a string or int.")

                flags = f

        compiled_pattern = re.compile(pattern, flags=flags)
        return compiled_pattern

    @classmethod
    def matches_rule(cls, uri: str, rule: RuleDataType) -> bool:
        if isinstance(rule, str):
            return (len(rule.strip()) > 0 and rule in uri)

        if isinstance(rule, dict):
            if "text" in rule:
                rule_text = rule["text"]
                if len(rule_text.strip()) > 0 and rule_text in uri:
                    return True

            if "regex" in rule:
                rule_regex = rule["regex"]
                compiled_pattern = cls.parse_regex(rule_regex)
                result = compiled_pattern.search(uri)
                return (result is not None)

        return False

    def find_rule(self, uri: str) -> tuple | None:
        browser_rules = self.browser_rules
        for browser_name in browser_rules:
            browser: dict = browser_rules[browser_name]
            if "rules" in browser:
                for rule in browser["rules"]:
                    if self.matches_rule(uri, rule):
                        return (browser, rule)
        return None


def launch_browser(browser: dict, uri: str, rule: RuleDataType) -> None:
    rule_clipboard = False

    if "path" in browser:
        path: str = os.path.expandvars(browser["path"])

        arguments = [path, uri]

        if "arguments" in browser:
            browser_arguments = browser["arguments"]
            arguments += (browser_arguments.split() if isinstance(browser_arguments, str) else browser_arguments)

        if isinstance(rule, dict):
            if "arguments" in rule:
                rule_arguments = rule["arguments"]
                arguments += (rule_arguments.split() if isinstance(rule_arguments, str) else rule_arguments)

            if "clipboard" in rule:
                rule_clipboard = rule["clipboard"]

        # print(arguments)
        subprocess.Popen(arguments)

    if rule_clipboard or ("clipboard" in browser and browser["clipboard"]):
        write_to_clipboard(uri)


def main(argv: list[str]) -> None:
    try:
        # print(argv)

        script_path = argv[0]
        uri = argv[1]

        change_to_file_directory(script_path)

        browser_rules = BrowserRules()

        result = browser_rules.find_rule(uri)
        browser = None
        rule = None
        if isinstance(result, tuple):
            browser = result[0]
            rule = result[1]
        else:
            browser = browser_rules.get_first_browser()

        launch_browser(browser, uri, rule)
    except Exception as exception:
        handle_exception(exception)


if __name__ == "__main__":
    main(sys.argv)