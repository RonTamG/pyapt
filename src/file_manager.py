import logging
import urllib
import urllib.request
from pathlib import Path

UPDATE_SUBDIRECTORY = "update"
PACKAGES_SUBDIRECTORY = "packages"


def url_into_saved_file_name(url):
    """
    the files from an apt update get saved to /var/lib/apt/lists.
    the names of the files are derived from the urls used to retrieve them.
    """
    return url.replace("http://", "").replace("/", "_")


class FileManager:
    def __init__(self, folder):
        self.folder = Path(folder)
        self.supported_compressions = [".xz", ".gz", ""]

    def get(self, url, name, directory=""):
        """
        send a get request to the specified url and return the response
        """
        saved_name = self.folder / directory / name
        if saved_name.exists():
            return saved_name

        request = urllib.request.Request(
            url,
            headers={"User-Agent": "Debian APT-HTTP"},
        )

        with urllib.request.urlopen(request) as response:
            if response.status == 200:
                self.save_file(name, response.read(), directory)
                return saved_name
            else:
                logging.warning(
                    f"failed to download {url} with status {response.status}"
                )
                return Path("")

    def get_update_file(self, url):
        for compression in self.supported_compressions:
            name = url_into_saved_file_name(url + compression)

            try:
                return self.get(url + compression, name, UPDATE_SUBDIRECTORY)
            except urllib.error.HTTPError:
                continue

        return ""

    def get_package_file(self, url):
        name = Path(url).name
        return self.get(url, name, PACKAGES_SUBDIRECTORY)

    def save_file(self, name, data, directory=""):
        """
        save a file to an optional subdirectory in the temp directory
        """
        # create directory if it doesn't exist
        update_directory = self.folder / directory
        update_directory.mkdir(parents=True, exist_ok=True)

        (update_directory / name).write_bytes(data)
