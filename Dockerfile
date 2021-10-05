FROM python:3.8-slim-buster

COPY . .

RUN apt update &&\
    apt install wget &&\
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - &&\
    sh -c echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list &&\
    apt-get -y update &&\
    apt-get install -y google-chrome-stable &&\
    wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip &&\
    apt-get install -yqq unzip &&\
    unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/ &&\
    DISPLAY=:99 &&\
    pip install dotascraper==0.0.4

CMD [ "python", "-m" , "dotaproscraper"" ]