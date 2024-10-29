FROM python:3.10-slim

RUN apt-get update \
    && apt-get -y install \
        git \
        sqlite3 \
    && pip install \
        discord.py \
        py-cord \
        sqlalchemy \
        asyncpg \
    && apt-get clean all \
    && rm -rf /var/lib/apt/lists/*

COPY --chmod=755 bot.py /
