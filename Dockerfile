# The container image: the checked wheel from CI, installed on a pinned Python base image.
FROM python:3.13-slim@sha256:e48f59cdba69a3cbd9ed2cf0f348d90d45a8d350d98134cf1070bc106ee9ed90
COPY dist/*.whl /tmp/
RUN python -m pip install --no-cache-dir /tmp/*.whl && rm /tmp/*.whl
USER nobody
ENTRYPOINT ["wordtally"]
