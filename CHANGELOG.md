## [1.6.1](https://github.com/RonTamG/pyapt/compare/v1.6.0...v1.6.1) (2023-11-11)


### Bug Fixes

* package dependency collection now ignores missing recommended packages ([42eb2b3](https://github.com/RonTamG/pyapt/commit/42eb2b366cf3899a163af526b87b50546ba94cfd))
* removed deletion of provides field in virtual package addition ([2f5cda4](https://github.com/RonTamG/pyapt/commit/2f5cda4070e4eae56f00d4d95a74e2f114b3f8b4))



# [1.6.0](https://github.com/RonTamG/pyapt/compare/v1.5.1...v1.6.0) (2023-09-13)


### Bug Fixes

* added run permissions to owner of install file in generated tar.gz file ([a5711ca](https://github.com/RonTamG/pyapt/commit/a5711ca17686763b019a1a5e5d98232d1871b646))
* progress bar correctly removes overflowing lines ([bcc0283](https://github.com/RonTamG/pyapt/commit/bcc02837ae11493b0a1af71526a151cd0ebc0e9f))


### Features

* added error message on missing sources list file ([57d9317](https://github.com/RonTamG/pyapt/commit/57d9317b85e318f4f88f7c83cd733583e7a52dda))
* changed user agent to debian apt ([0c84d07](https://github.com/RonTamG/pyapt/commit/0c84d0797674cb6b0ce74a9fa3efa759805bbfb5))
* fix added ansi escape character support in windows console ([9cf8b1b](https://github.com/RonTamG/pyapt/commit/9cf8b1b4573ffa513b914d423cf10b0b9b126ca3))



## [1.5.1](https://github.com/RonTamG/pyapt/compare/v1.5.0...v1.5.1) (2023-08-24)


### Bug Fixes

* added explicit encoding to Packages file write ([4cdfe04](https://github.com/RonTamG/pyapt/commit/4cdfe040158c131f1353853d9a23dfd902330c4b))
* multiline packages values with no data on first line ([f7d9adb](https://github.com/RonTamG/pyapt/commit/f7d9adb1281498a1c0c2b23ea99407929a8f28e2))
* parsing comments in sources list ([39cbff7](https://github.com/RonTamG/pyapt/commit/39cbff7885aa311be8aba7c3460451a6f13bd116))



# [1.5.0](https://github.com/RonTamG/pyapt/compare/v1.4.0...v1.5.0) (2023-08-19)


### Features

* added support for gzip compressed index files ([b75743c](https://github.com/RonTamG/pyapt/commit/b75743c3df1a8fdb49d550df24ea0c97d98b8377))
* removed unused download of InRelease files ([e8a0d92](https://github.com/RonTamG/pyapt/commit/e8a0d921ad3eedf6515e50965fec7e203f7839f5))



# [1.4.0](https://github.com/RonTamG/pyapt/compare/v1.3.0...v1.4.0) (2023-08-09)


### Features

* added new merged script release build ([62cc958](https://github.com/RonTamG/pyapt/commit/62cc9582da25ca7b9d7d27f5245e0b1b087efba9))



