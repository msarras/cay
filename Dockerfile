FROM python:3.12-slim-bookworm

WORKDIR /app

# Set the timezone
ENV TZ=America/Montreal
ARG NODE_MAJOR=18

RUN apt-get update \
  && apt-get install -y ca-certificates curl gnupg tzdata gettext \
  && mkdir -p /etc/apt/keyrings \
  && curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg \
  && echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list \
  && apt-get update \
  && apt-get install nodejs -y \
  && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man \
  && apt-get clean \
  && useradd --create-home python \
  && chown python:python -R /app

# Configure the timezone
RUN ln -fs /usr/share/zoneinfo/$TZ /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

USER python

COPY --chown=python:python requirements*.txt ./

RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED="true" \
    PATH="${PATH}:/home/python/.local/bin" \
    USER="python"

COPY --chown=python:python . .

WORKDIR /app

RUN python manage.py tailwind install --no-input;
RUN python manage.py tailwind build --no-input;

RUN npm install flowbite --prefix theme/static_src
RUN npm install apexcharts --save --save-dev --prefix theme/static_src
RUN npm install simple-datatables --save --save-dev --prefix theme/static_src

RUN python manage.py collectstatic --no-input
