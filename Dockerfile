FROM ghcr.io/astral-sh/uv:python3.13-alpine

WORKDIR /src

COPY src/pyproject.toml src/uv.lock .

RUN uv sync --frozen

COPY src/ .

ENTRYPOINT ["uv", "run", "main.py"]


