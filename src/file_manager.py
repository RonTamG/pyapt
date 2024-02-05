import gzip
import logging
import lzma
import urllib
import urllib.request
from pathlib import Path


def decompress(data, compression):
    """
    return the contents of a text file, supports xz, gz compressions
    """
    if compression == ".xz":
        return lzma.decompress(data).decode("utf-8")
    elif compression == ".gz":
        return gzip.decompress(data).decode("utf-8")
    else:
        return data


class FileManager:
    def __init__(self):
        self.supported_compressions = [".xz", ".gz", ""]

    def get(self, url):
        """
        send a get request to the specified url and return the response
        """
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "Debian APT-HTTP"},
        )

        with urllib.request.urlopen(request) as response:
            if response.status == 200:
                return response.read()
            else:
                logging.warning(
                    f"failed to download {url} with status {response.status}"
                )
                return ""

    def get_package_index_file(self, url):
        for compression in self.supported_compressions:
            try:
                compressed = self.get(url + compression)
            except urllib.error.HTTPError:
                continue

            return decompress(compressed, compression)

        return ""

    def get_package_file(self, url, directory):
        name = Path(url).name
        saved_name = Path(directory, name)
        if saved_name.exists():
            return saved_name
        else:
            saved_name.parent.mkdir(parents=True, exist_ok=True)
            content = self.get(url)
            saved_name.write_bytes(content)
            return saved_name
