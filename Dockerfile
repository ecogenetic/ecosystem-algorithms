FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt ./
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Critical CVE in zlib, temporarily include update until fixed in base
RUN apk update && \
    apk upgrade zlib

CMD [ "python"]