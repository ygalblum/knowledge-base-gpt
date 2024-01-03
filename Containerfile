ARG APP_ROOT=/app-root

FROM registry.fedoraproject.org/fedora:37 as build

ARG APP_ROOT

RUN dnf groupinstall --nodocs -y 'Development Tools' && \
    dnf install --nodocs -y python-pip python-devel g++ &&\
    dnf clean all -y

WORKDIR ${APP_ROOT}

COPY ./dist/knowledge_base_gpt*.whl /tmp/

RUN python3 -m venv ${APP_ROOT}/venv \
    && source ${APP_ROOT}/venv/bin/activate \
    && pip install --no-cache-dir -U pip wheel \
    && pip install --no-cache-dir /tmp/knowledge_base_gpt*.whl \
    && echo "unset BASH_ENV PROMPT_COMMAND ENV" >> ${APP_ROOT}/venv/bin/activate

FROM registry.fedoraproject.org/fedora:37

ARG APP_ROOT

WORKDIR ${APP_ROOT}

COPY --from=build ${APP_ROOT}/venv ${APP_ROOT}/venv

# activate virtualenv with workaround RHEL/CentOS 8+
ENV BASH_ENV="${APP_ROOT}/venv/bin/activate" \
    ENV="${APP_ROOT}/venv/bin/activate" \
    PROMPT_COMMAND=". ${APP_ROOT}/venv/bin/activate" \
    PATH="${APP_ROOT}/venv/bin:${PATH}"

CMD ["python", "-m", "knowledge_base_gpt.apps.slackbot.slack_bot"]
