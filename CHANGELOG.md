# [1.4.0](https://github.com/RonTamG/pyapt/compare/v1.3.0...v1.4.0) (2023-08-09)


### Features

* added new merged script release build ([62cc958](https://github.com/RonTamG/pyapt/commit/62cc9582da25ca7b9d7d27f5245e0b1b087efba9))



# [1.3.0](https://github.com/RonTamG/pyapt/compare/v1.2.0...v1.3.0) (2023-08-07)


### Features

* added execute permissions to install.sh file in tar ([cb6bb33](https://github.com/RonTamG/pyapt/commit/cb6bb339f1534fa786db0c750c940c9336f80c8b))
* install script uses new list in sources.list.d and updates only it ([c9094c7](https://github.com/RonTamG/pyapt/commit/c9094c779807f1d28192ccb2ffc08223eee24be1))



# [1.2.0](https://github.com/RonTamG/pyapt/compare/v1.1.0...v1.2.0) (2023-08-06)


### Features

* added cleanup of install script ([6259705](https://github.com/RonTamG/pyapt/commit/625970566360352f61b8c8c4dbfd339645003892))
* install script now uses apt install from local repo ([2ad0e3d](https://github.com/RonTamG/pyapt/commit/2ad0e3de146138659ec20bb687e3055c201e43df))
* removed change to Package keys names in index ([0554468](https://github.com/RonTamG/pyapt/commit/05544689d78f49b58759a8fa14b7d768da368213))



# [1.1.0](https://github.com/RonTamG/pyapt/compare/v1.0.0...v1.1.0) (2023-07-31)


### Bug Fixes

* fixed deprecation warnings in update regex ([f07ce9a](https://github.com/RonTamG/pyapt/commit/f07ce9a3d7f228a44a178e34d7a9fb5cde4f5c12))


### Features

* added linter formatter and type checking ([0e53ab5](https://github.com/RonTamG/pyapt/commit/0e53ab528d8a7365616679dd90343c58968f0e2b))



# [1.0.0](https://github.com/RonTamG/pyapt/compare/6b78439443fd32f58892e7f56e8cb570d04c2dd8...v1.0.0) (2023-03-25)


### Bug Fixes

* changed url joins to use posixpath instead of os.path ([95aba67](https://github.com/RonTamG/pyapt/commit/95aba67a0b5263172b3eef519744aa6553fe3d54))
* **main:** names of existing files returned in download packages no longer include full path ([2128d92](https://github.com/RonTamG/pyapt/commit/2128d923dd86731d5591452b34e4c0110af446c5))
* **packages:** fixed appending to iterated list ([c9dfe0b](https://github.com/RonTamG/pyapt/commit/c9dfe0b836df8825a0d9cc90eaf63a5f6bf9d5c8))
* **packages:** fixed pre depends option not used in get package dependencies ([ff9e291](https://github.com/RonTamG/pyapt/commit/ff9e291f8fa5100491ecb6c53b5fa401ee486e6c))


### Features

* added basic apt-get implementation ([6b78439](https://github.com/RonTamG/pyapt/commit/6b78439443fd32f58892e7f56e8cb570d04c2dd8))
* **install:** added create install script function ([3c24053](https://github.com/RonTamG/pyapt/commit/3c24053d475cd2ab8c47b0e8e38bb19c5d0167ff))
* **install:** added refuse downgrade and no download ([d1f1755](https://github.com/RonTamG/pyapt/commit/d1f1755f4ecc212f0f41eb1ccb5d45708d318215))
* **main:** added --with-required option ([d093de9](https://github.com/RonTamG/pyapt/commit/d093de973db60751d5c43264f72295c3acbd2c9a))
* **main:** added deletion of temp directory after tar ([727fc4f](https://github.com/RonTamG/pyapt/commit/727fc4f43dfd2b2563762cabacfdbf30c553736f))
* **main:** added keep update argument ([e3931ee](https://github.com/RonTamG/pyapt/commit/e3931ee1fd40d0c9ddbfa17430c0ed7057d58842))
* **main:** added no download of already existing file ([54b2150](https://github.com/RonTamG/pyapt/commit/54b2150da9fb4f3b208782647d50ab7d7697f953))
* **main:** added options to not download dependencies or recommended ([4e1ded2](https://github.com/RonTamG/pyapt/commit/4e1ded2a341a8b1cbdca6628a0354fa0c6d7cc6c))
* **main:** added sources list argument ([8952714](https://github.com/RonTamG/pyapt/commit/8952714d88a6dea73997d13e08ef1e1a8359a1f3))
* **main:** added support for multiple package downloads ([6c64443](https://github.com/RonTamG/pyapt/commit/6c64443dbe128d33681a4c32f0a51d440cc3a396))
* **main:** added temp folder argument ([3753564](https://github.com/RonTamG/pyapt/commit/3753564435104d1699b47517b4d28accc033cd39))
* **main:** changed progress bar to use ansi escape chars ([2edf024](https://github.com/RonTamG/pyapt/commit/2edf024e2e01b95b69bebe69b37c4f8239c072aa))
* **main:** refactored apt download implementation ([9354e82](https://github.com/RonTamG/pyapt/commit/9354e82d6f47adcecb91b3cc3a2deea359ac98a6))
* **name:** added progress bars to update and package downloads ([17e7ba6](https://github.com/RonTamG/pyapt/commit/17e7ba62723fbf45e634e9198e0f4fb897720ef2))
* **packages:** added get package dependencies ([5fb0a84](https://github.com/RonTamG/pyapt/commit/5fb0a844d29eb1b7b538331c866be574226df14c))
* **packages:** added get package url ([80aa715](https://github.com/RonTamG/pyapt/commit/80aa7151ec7815cc2e006ac406d7a1913e173d0d))
* **packages:** removed packages with priority required or importand by default ([4d64ebd](https://github.com/RonTamG/pyapt/commit/4d64ebd58df089b4ab15d92e4b4c3be94d81654e))
* **update:** added an apt source field to packages in index ([db882f9](https://github.com/RonTamG/pyapt/commit/db882f930b402e3010f6c580be0e4ac92e24e90b))
* **update:** added apt sources from url function ([b4877f6](https://github.com/RonTamG/pyapt/commit/b4877f61c65664ba3cb9557078aa182ff7d8ef31))
* **update:** added debian version comparison ([f9dfb43](https://github.com/RonTamG/pyapt/commit/f9dfb43c5fd0b5b10a5cf9b3f4474325006ad69d))
* **update:** added index dictionary generation ([b97e069](https://github.com/RonTamG/pyapt/commit/b97e069cd491726387c09abee9de0431e9f2104c))
* **update:** added index url generation ([70dda2f](https://github.com/RonTamG/pyapt/commit/70dda2f017c39e1c95f71904df1d438f01c5d8ec))
* **update:** added release url generation ([8039647](https://github.com/RonTamG/pyapt/commit/8039647609b97d965035ad938e9c088358892b5f))
* **update:** added source list parsing ([2b88bfd](https://github.com/RonTamG/pyapt/commit/2b88bfd80ab0f9755668b92e4d312fcbe6322a1c))
* **update:** added split debian version function ([dd4eaeb](https://github.com/RonTamG/pyapt/commit/dd4eaeb285806328a6c8c23c0836825dd5fd5ecc))
* **update:** added support for virtual packages ([b83e941](https://github.com/RonTamG/pyapt/commit/b83e941dd07e22229a2972697ccb8abb5a4f7b29))
* **update:** added test for multiline fields in index generation ([1e34131](https://github.com/RonTamG/pyapt/commit/1e341317e7c9d1cf72d2b9719fbc9dcb3f19d0c6))
* **update:** added url into saved file name ([d760481](https://github.com/RonTamG/pyapt/commit/d760481b92530208dfb12091291307315ffc1a86))
* **update:** changed index creation to include only latest versions ([335730b](https://github.com/RonTamG/pyapt/commit/335730b25d245ce45ebb50d53e3e767ada424440))



