FROM python:3.12-slim AS build

WORKDIR /app

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
  pip install --no-cache-dir -r requirements.txt

FROM python:3.12-slim

WORKDIR /app

COPY --from=build /opt/venv /opt/venv


COPY . .
COPY entrypoint.sh /exerciseAPI/entrypoint.sh
RUN chmod +x /exerciseAPI/entrypoint.sh

ENV PATH="/opt/venv/bin:$PATH"

EXPOSE 8000

ENTRYPOINT [ "exerciseAPI/entrypoint.sh" ]
CMD ["uvicorn", "exerciseAPI.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers","4"]