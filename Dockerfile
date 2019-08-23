FROM python:3.6-alpine

RUN adduser -D microblog

WORKDIR /home/microblog

COPY requirements.txt run_blog.py config.py boot.sh ./

RUN python -m venv venv
RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY blog_app blog_app

COPY migrations migrations

ENV FLASK_APP run_blog.py

RUN chown -R microblog:microblog ./

USER microblog

EXPOSE 5000

CMD ["./boot.sh"]
