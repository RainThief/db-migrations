FROM python:3.8-alpine3.12 AS builder

RUN apk add --no-cache \
    curl=7.69.1-r3 \
    gcc=9.3.0-r2 \
    postgresql-dev=12.5-r0\
    musl-dev=1.1.24-r10 \
    python3-dev=3.8.5-r0

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

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt


FROM python:3.8-alpine3.12

COPY --from=builder /usr/local/bin/hadolint /usr/local/bin/hadolint

COPY --from=builder /usr/local/bin/shellcheck /usr/local/bin/shellcheck

COPY --from=builder /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages

COPY --from=builder /usr/local/bin /usr/local/bin

RUN apk add --no-cache \
    bash=5.0.17-r0 \
    git=2.26.2-r0 \
    jq=1.6-r1 \
    curl=7.69.1-r3 \
    postgresql=12.5-r0; \
    mkdir -p /.cache/pip && chmod 666 -Rc /.cache

WORKDIR /usr/app
