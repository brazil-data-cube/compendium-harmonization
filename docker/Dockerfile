#
FROM python@sha256:3bc519ca3214d463ac521f838275e1070ab4b8dbb12e568b4739794db837dadb

EXPOSE 3000

ENV DAGSTER_APP=/opt/dagster/app/
ENV DAGSTER_HOME=/opt/dagster/dagster_home/
ENV DAGSTER_LOCAL_STORAGE=/opt/dagster/storage/

#
# Create base directories
#
RUN mkdir -p $DAGSTER_APP $DAGSTER_HOME

#
# Copy the article analysis files.
#
COPY analysis $DAGSTER_APP

COPY cfactor /opt/article/cfactor
COPY setup.py /opt/article/setup.py

COPY docker/config/dagster.yaml $DAGSTER_HOME/dagster.yaml
COPY docker/config/workspace.yaml $DAGSTER_APP/workspace.yaml

#
# Install dependencies
#
RUN pip install --upgrade \
    pip \
    setuptools \
    wheel \
    && pip install \
        dagit==0.12.2 \
        numpy==1.21.1 \
        dagster==0.12.2 \
        rasterio==1.2.6 \
        matplotlib==3.4.2 \
        shapely==1.7.1 \
    && cd /opt/article/ \
    && python3 setup.py install \
    && apt update -y \
    && apt install curl -y \
    && curl -fsSL https://get.docker.com | sh

WORKDIR $DAGSTER_APP

ENTRYPOINT ["dagit", "-h", "0.0.0.0", "-p", "3000"]
