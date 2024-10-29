FROM python:3.10-slim

RUN pip install \
    discord.py \
    py-cord \
    sqlalchemy \
    asyncpg

COPY --chmod=755 bot.py /
