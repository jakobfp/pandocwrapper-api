FROM python:3

COPY /pandocwrapper /pandocwrapper

WORKDIR /pandocwrapper

RUN pip install .

WORKDIR .

COPY /pandocwrapper-api /api

WORKDIR /api

RUN pip install --trusted-host pypi.python.org -r requirements.txt

RUN wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1ZxGUaY8by0ESU4GciZaCX4UmcjAhSmDU' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1ZxGUaY8by0ESU4GciZaCX4UmcjAhSmDU" -O cis.tar.gz && rm -rf /tmp/cookies.txt

RUN tar -zxvf cis.tar.gz

RUN rm cis.tar.gz

EXPOSE 5000

CMD ["python", "app.py"]
