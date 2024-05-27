FROM python:3.12-alpine

RUN wget https://download.microsoft.com/download/3/5/5/355d7943-a338-41a7-858d-53b259ea33f5/msodbcsql18_18.3.3.1-1_amd64.apk
RUN wget https://download.microsoft.com/download/3/5/5/355d7943-a338-41a7-858d-53b259ea33f5/mssql-tools18_18.3.1.1-1_amd64.apk

RUN apk add --allow-untrusted msodbcsql18_18.3.3.1-1_amd64.apk mssql-tools18_18.3.1.1-1_amd64.apk
RUN rm msodbcsql18_18.3.3.1-1_amd64.apk mssql-tools18_18.3.1.1-1_amd64.apk

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
