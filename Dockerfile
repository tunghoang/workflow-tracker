FROM python:3.9.20

ENV DEBIAN_FRONTEND=noninteractive \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    TINI_VERSION=v0.19.0

ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini

RUN apt-get update && \
    apt-get install -y \
      libpq-dev \
      wget \
      vim \
    && apt-get autoclean \
    && apt-get autoremove \
    && rm -rf /var/lib/{apt,dpkg,cache,log}

COPY requirements.txt /conf/
RUN pip install --no-cache-dir --requirement /conf/requirements.txt

RUN useradd admin

WORKDIR /app

ENTRYPOINT ["/tini", "--"]

CMD ["gunicorn", "--config", "gconfig.py", "app:app"]

