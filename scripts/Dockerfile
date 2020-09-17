FROM python:3.8-slim-buster

COPY requirements.txt requirements.txt

RUN  apt-get update &&  apt-get install -y --no-install-recommends \
    libpq-dev=11.7-0+deb10u1 \
    libc6-dev=2.28-10 \
    gcc=4:8.3.0-1 \
    curl=7.64.0-4+deb10u1 \
    xz-utils=5.2.4-1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

# install hadolint (Dockerfile linter)
RUN curl -L "https://github.com/hadolint/hadolint/releases/latest/download/hadolint-Linux-x86_64"  -o "hadolint" \
  && chmod +x hadolint \
  && mv hadolint /usr/local/bin/hadolint

# install shellcheck (bash linter)
RUN curl -L "https://github.com/koalaman/shellcheck/releases/download/v0.7.1/shellcheck-v0.7.1.linux.x86_64.tar.xz"  -o "shellcheck.tar.xz" \
  && tar xf shellcheck.tar.xz \
  && mv shellcheck-v0.7.1/shellcheck /usr/local/bin/shellcheck \
  && chmod +x /usr/local/bin/shellcheck \
  && rm -Rf shellcheck*

RUN apt-get purge -y gcc libpq-dev curl xz-utils && apt-get autoremove -y && rm -Rf /var/cache/apt

WORKDIR /usr/app
