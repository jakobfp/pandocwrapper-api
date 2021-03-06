# pandocwrapper-api

**Created for an university course at HTW BERLIN.**

WEB-API for [pandocwrapper](https://github.com/jakobfp/pandocwrapper). With some additional functionalities (check the [docs](#documentation)).

### Requirements

[pandocwrapper](https://github.com/jakobfp/pandocwrapper) (check README for setup) and packages in [requirements](./requirements.txt)

You need to download the [CI templates](https://drive.google.com/uc?export=download&id=1ZxGUaY8by0ESU4GciZaCX4UmcjAhSmDU) and unpack them in the project root directory:
```
pandocwrapper-api
│   
└───cis
│   │   htwberlin.tex
│   │   htwberlin-beamer.tex
│   │   htw-background.png
│   │   htw-logo-foot.png
│   │   htw-logo-titel.jpg
│   └───fonts
│       │   ...
│   ...   

```
**Also add new templates in this directory!**

### Start API

`$ python app.py` is enough to let the application serve at [localhost:5000/api](localhost:5000/api).

### Documentation

#### WebAPI
After starting it got to [localhost:5000/api/ui](localhost:5000/api/ui).

#### Modules
Find the documentation of the modules here: [https://jakobfp.github.io/pandocwrapper-api/](https://jakobfp.github.io/pandocwrapper-api/)


