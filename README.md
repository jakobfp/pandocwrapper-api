# pandocwrapper-api

REST-API for [pandocwrapper](https://github.com/jakobfp/pandocwrapper). With some additional functionalities (check the [docs](#documentation)).

### Requirements

[pandocwrapper](https://github.com/jakobfp/pandocwrapper) (check README for setup) and packages in [requirements](./requirements.txt)

You need to download the [CI templates](http://s000.tinyupload.com/?file_id=22689526233418835186) and unzip them in the project root directory:
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

#### RestAPI
After starting it got to [localhost:5000/api/ui](localhost:5000/api/ui).

#### Modules
Find the documentation of the modules here: [https://jakobfp.github.io/pandocwrapper-api/](https://jakobfp.github.io/pandocwrapper-api/)
