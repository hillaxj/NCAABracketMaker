FROM python:3.10 AS base

FROM base AS requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

FROM requirements AS final
WORKDIR /usr/src/app
COPY . .
