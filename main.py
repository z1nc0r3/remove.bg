# Author: Lasith Manujitha
# Github: @z1nc0r3
# Description: A simple plugin to shorten URLs using tinyurl.com
# Date: 2024-02-04

import sys, os

parent_folder_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(parent_folder_path)
sys.path.append(os.path.join(parent_folder_path, "lib"))
sys.path.append(os.path.join(parent_folder_path, "plugin"))

from flowlauncher import FlowLauncher
import webbrowser
import requests
import pyperclip
import re


class Shortener(FlowLauncher):

    def isValidURL(self, str):
        regex = (
            "((http|https)://)(www.)?"
            + "[a-zA-Z0-9@:%._\\+~#?&//=]"
            + "{1,256}\\.[a-z]"
            + "{2,6}\\b([-a-zA-Z0-9@:%"
            + "._\\+~#?&//=]*)"
        )

        p = re.compile(regex)

        if re.search(p, str):
            return True
        else:
            return False

    def query(self, query):
        output = []
        if len(query.strip()) == 0:
            output.append(
                {"Title": "Enter a URL to shorten", "IcoPath": "Images/app.png"}
            )

        else:

            if not (query.startswith("http://") or query.startswith("https://")):
                query = f"https://{query}"

            api_url = f"https://tinyurl.com/api-create.php?url={query}"

            try:
                if not self.isValidURL(query):
                    raise ValueError

                response = requests.get(api_url)
                tiny = response.text

                if tiny == "Error":
                    raise Exception
            except Exception:
                output.append(
                    {
                        "Title": "Error: Enter a valid URL",
                        "IcoPath": "Images/broken.png",
                    }
                )
                return output

            output.append(
                {
                    "Title": "Click to copy",
                    "SubTitle": f"{tiny}",
                    "IcoPath": "Images/copy.png",
                    "JsonRPCAction": {"method": "copy", "parameters": [f"{tiny}"]},
                }
            )

            output.append(
                {
                    "Title": "Click to open in browser",
                    "SubTitle": f"{tiny}",
                    "IcoPath": "Images/open.png",
                    "JsonRPCAction": {"method": "open_url", "parameters": [f"{tiny}"]},
                }
            )

        return output

    def copy(self, tiny):
        pyperclip.copy(tiny)

    def open_url(self, url):
        webbrowser.open(url)


if __name__ == "__main__":
    Shortener()
