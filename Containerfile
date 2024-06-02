FROM registry.fedoraproject.org/fedora:41 as builder

RUN dnf groupinstall --nodocs -y 'Development Tools' && \
    dnf install --nodocs -y python-pip python-devel g++ && \
    dnf clean all -y

RUN pip install poetry

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --no-root

FROM registry.fedoraproject.org/fedora:41 as runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

RUN dnf install --nodocs -y jq && \
    dnf clean all -y

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY knowledge_base_gpt/ ./knowledge_base_gpt

ENTRYPOINT ["python", "-m", "knowledge_base_gpt.apps.slackbot"]
