# [1.10.0](https://github.com/RonTamG/pyapt/compare/v1.9.0...v1.10.0) (2024-02-12)


### Bug Fixes

* added downloading of packages with required and important priority ([aa84d97](https://github.com/RonTamG/pyapt/commit/aa84d97100cbcbefa82b51f1eabdc39e8f243979))


### Features

* changed name of inner folder of output tar to be name of tar instead of temp folder name ([ba93cfa](https://github.com/RonTamG/pyapt/commit/ba93cfa0bf90b56805922f58e2aef85d3ae9769f))



# [1.9.0](https://github.com/RonTamG/pyapt/compare/v1.8.2...v1.9.0) (2024-02-07)


### Bug Fixes

* missing match check in virtual package name parsing ([4fcbe06](https://github.com/RonTamG/pyapt/commit/4fcbe060903b6a37e97d2b9891e60b82ccd18cfd))
* version int upstream compare fillvalue was string instead of int ([54d80e6](https://github.com/RonTamG/pyapt/commit/54d80e630df711c83bb4fc69b87137ddbb99a867))


### Features

* added saving index to --keep ([71f0205](https://github.com/RonTamG/pyapt/commit/71f0205889145593ce661be53a0f42f9a6bfcb39))
* added support for alternative dependencies in index search ([9e0a62d](https://github.com/RonTamG/pyapt/commit/9e0a62df59f295f152cc87bad45dff86a8100e67))
* added version handling for virtual packages ([aad680e](https://github.com/RonTamG/pyapt/commit/aad680e868ed629f9e906f323752b2c09c5f386d))



## [1.8.2](https://github.com/RonTamG/pyapt/compare/v1.8.1...v1.8.2) (2024-02-06)


### Bug Fixes

* fixed merged python artifact ([0bb398e](https://github.com/RonTamG/pyapt/commit/0bb398e010397c0a8fdec509e4fe06d5f6d1eff5))



## [1.8.1](https://github.com/RonTamG/pyapt/compare/v1.8.0...v1.8.1) (2024-02-06)


### Bug Fixes

* fixed merged python artifact ([941f956](https://github.com/RonTamG/pyapt/commit/941f95692b1bb387c8e6af547fe4530af6d47d17))



# [1.8.0](https://github.com/RonTamG/pyapt/compare/v1.7.0...v1.8.0) (2024-02-06)


### Bug Fixes

* changed default package apt source to empty string ([b0d256d](https://github.com/RonTamG/pyapt/commit/b0d256d48d360c761de8bbbf4cc69f599d65499e))
* debian version comparison of digits compared them one by one ([78e70cc](https://github.com/RonTamG/pyapt/commit/78e70cc4dc0f370067b6ff987e31cc388fa04f0b))


### Features

* added apt source field to package ([292acb4](https://github.com/RonTamG/pyapt/commit/292acb4a128ee529e8b489676b05f1e2b8c07f8e))
* added architecture field to package ([2b5c317](https://github.com/RonTamG/pyapt/commit/2b5c317906217b86c0b89a21f64c125dcee64956))
* added contains check to index ([c30bbb8](https://github.com/RonTamG/pyapt/commit/c30bbb8b14d9f25d9e97daaae75acb116214b56f))
* added default optional priority to package ([891f67c](https://github.com/RonTamG/pyapt/commit/891f67c1a222451c5d0da6dfb0bb30a7ef7394d6))
* added dependencies field to package ([c888006](https://github.com/RonTamG/pyapt/commit/c888006590bdfd8356b8e84c00c4ff3a7951d79a))
* added dependency search with recommended packages ([d590db3](https://github.com/RonTamG/pyapt/commit/d590db3382a11dfc38733f592d1dccc34aff2a47))
* added description field to package ([ff9199c](https://github.com/RonTamG/pyapt/commit/ff9199cac54d04e8b8c4b6b93163111e9272c775))
* added download url field to package ([ebaa8e6](https://github.com/RonTamG/pyapt/commit/ebaa8e69161a84b7950d6fad13d9c46656aae50e))
* added earlier or equal search to index ([5a96592](https://github.com/RonTamG/pyapt/commit/5a96592c404d5b5b8bac0556c90eff5063592400))
* added empty provides list in package ([f7f4681](https://github.com/RonTamG/pyapt/commit/f7f4681651ff136cb37d11d7cccb34b69086a202))
* added function to set apt source field of packages in an index ([7b2e1f7](https://github.com/RonTamG/pyapt/commit/7b2e1f7c8919868c26c769de432aecd8fea0072b))
* added greater than to version comparison ([8f0cb44](https://github.com/RonTamG/pyapt/commit/8f0cb446babe48a15066f7f3b5f1b53aafc1fc57))
* added index class ([d12ae8c](https://github.com/RonTamG/pyapt/commit/d12ae8c333b73cd66c8a18f7fc868aa2f0b5819b))
* added index combining ([b273de0](https://github.com/RonTamG/pyapt/commit/b273de0c4a71fb4588827b5025b944cf958c4086))
* added later or equal version search to index ([225324b](https://github.com/RonTamG/pyapt/commit/225324b02bc8212754afd8bf3766c5dd88035c40))
* added less than to version comparison ([fed6980](https://github.com/RonTamG/pyapt/commit/fed6980176eba7431a48fedd5a7a0745c4ef68bd))
* added maintainer field to package ([648935e](https://github.com/RonTamG/pyapt/commit/648935e9069a5dc6dd00d1d70591ddb343e8a006))
* added multiple package parsing for index ([516a1c4](https://github.com/RonTamG/pyapt/commit/516a1c4fc014b348341199afad13c76cc8ecd3f3))
* added multiple package versions to index ([0d55953](https://github.com/RonTamG/pyapt/commit/0d559539fab5c254d24c4a85830e40e54b297089))
* added package class ([6db6317](https://github.com/RonTamG/pyapt/commit/6db6317b0bdcdd471b2e24afcfa91649baad77aa))
* added package comparison ([33cdf80](https://github.com/RonTamG/pyapt/commit/33cdf80fc35135a859b84b34f114099eda2f0732))
* added package dependency search in index ([4b16bff](https://github.com/RonTamG/pyapt/commit/4b16bff268506e2568651381df1624fe36611e6e))
* added pre dependencies field to package ([77ecc64](https://github.com/RonTamG/pyapt/commit/77ecc644642693cdf889ba7870587525ed04bd4e))
* added priority field to package ([e64913f](https://github.com/RonTamG/pyapt/commit/e64913f3b3182d8605460d578dd0ab43d6d451d7))
* added provides list to package ([903781c](https://github.com/RonTamG/pyapt/commit/903781cc3e30843ad0affba7322154a145601e4f))
* added recommended field to package ([cfe15e1](https://github.com/RonTamG/pyapt/commit/cfe15e1b11381ca648845854c2df620dda21bb27))
* added repr to package ([eb95f8b](https://github.com/RonTamG/pyapt/commit/eb95f8bad5fd8a16dbcbc6078e44351aa37f2b20))
* added repr to version ([1372599](https://github.com/RonTamG/pyapt/commit/1372599b217c33368ee2a2efab0b9aefbc648d0a))
* added return to original string form for package ([2c3abf3](https://github.com/RonTamG/pyapt/commit/2c3abf39410158209cc3967a26f2ed509872cbc0))
* added search by name to index ([a996cfa](https://github.com/RonTamG/pyapt/commit/a996cfac2c1159a799c090280cf003e019a1919e))
* added search by version to index ([518b4b3](https://github.com/RonTamG/pyapt/commit/518b4b341bd1ff1556627df97b6d400d17ef7a40))
* added searching by earlier version to index ([958cd3c](https://github.com/RonTamG/pyapt/commit/958cd3c96bcfa1883647a85bbf51115e97c45393))
* added searching by later version to index ([200adbc](https://github.com/RonTamG/pyapt/commit/200adbcd5dcceb3d42793c4abc89fd00cf4f9b30))
* added sorting to multiple package versions in index ([d604131](https://github.com/RonTamG/pyapt/commit/d60413185a288b0454286617bb52dfa298962188))
* added Version class ([5050507](https://github.com/RonTamG/pyapt/commit/5050507811a8931272e83b113bd0a9463fb367cf))
* added version info to package ([a382ff3](https://github.com/RonTamG/pyapt/commit/a382ff3304dcd21a29a0e374bff5d3cb9fac6dbb))
* added virtual package support for index ([0efe830](https://github.com/RonTamG/pyapt/commit/0efe83015e695e0dd8e7d2dae6f5d9b0c9b3a594))
* added with_item boolean to progress bar ([b3c0ae2](https://github.com/RonTamG/pyapt/commit/b3c0ae25f28cb6d2511f4e8ed81800c1358bbc9c))
* hash function for version ([b53f45b](https://github.com/RonTamG/pyapt/commit/b53f45b334a69e498a1e3b1be2eb265624d99c43))
* index search ignores architecture qualifier ([12fbbff](https://github.com/RonTamG/pyapt/commit/12fbbff8732931ac233c4705bfce80aa49d85a9b))
* set return value of set_package_apt_source method of index to self ([89a8e4b](https://github.com/RonTamG/pyapt/commit/89a8e4b4d055eac8e743264a979e2579890ce202))



