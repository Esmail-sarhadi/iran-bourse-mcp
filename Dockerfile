FROM python:3.12-slim

LABEL org.opencontainers.image.title="iran-bourse-mcp" \
      org.opencontainers.image.description="MCP server for Tehran Stock Exchange (TSETMC) and Codal data" \
      org.opencontainers.image.source="https://github.com/msmahdinejad/iran-bourse-mcp" \
      org.opencontainers.image.licenses="MIT"

WORKDIR /app
COPY pyproject.toml README.md LICENSE ./
COPY src ./src
RUN pip install --no-cache-dir . && useradd --create-home bourse
USER bourse

# stdio by default (what MCP clients launch):  docker run -i --rm iran-bourse-mcp
# HTTP:  docker run -p 8000:8000 --rm iran-bourse-mcp serve --transport streamable-http --host 0.0.0.0
ENTRYPOINT ["iran-bourse-mcp"]
