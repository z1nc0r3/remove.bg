# Author: Lasith Manujitha
# Github: @z1nc0r3
# Description: Remove background from images using remove.bg API
# Date: 2024-03-28

import sys, os

parent_folder_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(parent_folder_path)
sys.path.append(os.path.join(parent_folder_path, "lib"))
sys.path.append(os.path.join(parent_folder_path, "plugin"))

from flowlauncher import FlowLauncher
import requests
from pathlib import Path
import re


class Remover(FlowLauncher):

    def is_valid_file(self, file):
        supported = [".jpg", ".jpeg", ".png", ".pjp", ".pjpeg"]
        
        if Path(file).suffix.lower() not in supported:
            return False

        return os.path.isfile(file)

    def is_valid_url(self, str):
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
                {"Title": "Enter a file path or URL", "IcoPath": "Images/app.png"}
            )

        else:
            file = query.strip()
            file = file.replace('"', "")
            save_path = os.path.expanduser("~/Downloads")

            if self.is_valid_file(file):
                file_name = Path(file).stem
                files = {"image_file": open(file, "rb")}
                data = {"size": "auto"}

            elif self.is_valid_url(file):
                file_name = os.path.basename(file).split("?")[0]
                files = None

                if requests.head(file).status_code != 200:
                    file = file.split("?")[0]

                data = {"image_url": file}

            else:
                output.append(
                    {
                        "Title": "Invalid file path or URL",
                        "IcoPath": "Images/error.png",
                    }
                )

                return output

            response = requests.post(
                "https://api.remove.bg/v1.0/removebg",
                files=files,
                data=data,
                headers={"X-Api-Key": "jNAnhZ5d5DFU4bRQZD7YhaYf"},
            )

            if response.status_code == 200:
                file_name = file_name.replace(" ", "_")
                
                with open(f"{save_path}/{file_name}.png", "wb") as out:
                    out.write(response.content)

                output.append(
                    {
                        "Title": "Click to open the image location",
                        "SubTitle": "Background removed successfully",
                        "IcoPath": "Images/open_dir.png",
                        "JsonRPCAction": {
                            "method": "open_dir",
                            "parameters": [save_path],
                        },
                    }
                )

                output.append(
                    {
                        "Title": "Click to open the image",
                        "SubTitle": "Background removed successfully",
                        "IcoPath": "Images/app.png",
                        "JsonRPCAction": {
                            "method": "open",
                            "parameters": [f"{save_path}/{file_name}.png"],
                        },
                    }
                )

            else:
                output.append(
                    {
                        "Title": "Failed to remove background",
                        "SubTitle": "Please check the file or URL and try again",
                        "IcoPath": "Images/error.png",
                    }
                )

        return output

    def open(self, file_name):
        os.system(f"start {file_name}")

    def open_dir(self, save_path):
        os.system(f"start {save_path}")


if __name__ == "__main__":
    Remover()
