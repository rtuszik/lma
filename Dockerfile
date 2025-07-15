FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

RUN groupadd -r app && useradd -r -g app app

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project

COPY . .

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-editable --compile-bytecode

RUN chown -R app:app /app

# Create cache directory for app user
RUN mkdir -p /home/app/.cache/uv && chown -R app:app /home/app/.cache

USER app

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app"

EXPOSE 6969

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:6969/ || exit 1

CMD ["uv", "run", "main.py"]
