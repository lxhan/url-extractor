FROM python:3.10

WORKDIR /app

RUN apt update -y && apt upgrade -y \
  && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
  && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
  && apt update -y \
  && apt install google-chrome-stable -y \
  && DRIVER_VERSION=$(curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE) \
  && wget "https://chromedriver.storage.googleapis.com/${DRIVER_VERSION}/chromedriver_linux64.zip" \
  && unzip chromedriver_linux64.zip \
  && mv chromedriver /usr/bin/chromedriver \
  && chmod +x /usr/bin/chromedriver

COPY requirements.txt .

RUN python3 -m pip install -r requirements.txt

COPY . .

CMD ["python3", "main.py"]