from src.file_manager import url_into_saved_file_name


def test_url_turn_into_saved_file_name_is_successful():
    urls = [
        "http://deb.debian.org/debian/dists/bullseye/InRelease",
        "http://deb.debian.org/debian/dists/bullseye/main/binary-amd64/Packages.xz",
        "http://security.debian.org/debian-security/dists/bullseye-security/InRelease",
        "http://security.debian.org/debian-security/dists/bullseye-security/main/binary-amd64/Packages.xz",
    ]

    expected_names = [
        "deb.debian.org_debian_dists_bullseye_InRelease",
        "deb.debian.org_debian_dists_bullseye_main_binary-amd64_Packages.xz",
        "security.debian.org_debian-security_dists_bullseye-security_InRelease",
        "security.debian.org_debian-security_dists_bullseye-security_main_binary-amd64_Packages.xz",
    ]

    result = [url_into_saved_file_name(url) for url in urls]

    assert result == expected_names
