FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY pyproject.toml ./
COPY src ./src
RUN pip install --no-cache-dir . \
    && groupadd --gid 10001 mergen \
    && useradd --uid 10001 --gid mergen --create-home --shell /usr/sbin/nologin mergen
USER 10001:10001
EXPOSE 8080
CMD ["uvicorn", "mergen.main:app", "--host", "0.0.0.0", "--port", "8080"]
