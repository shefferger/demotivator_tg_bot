FROM python:3.10 AS builder
COPY requirements.txt .
RUN python3 -m venv /venv
ENV PATH=/venv/bin:$PATH
RUN pip install -r requirements.txt

FROM python:3.10-slim
RUN useradd --create-home appuser
USER appuser
WORKDIR /app
COPY app /app
COPY --from=builder --chown=appuser /venv /app/venv
ENV PATH=/app/venv/bin:$PATH
CMD ["python3", "main.py"]
