FROM node:24-alpine AS frontend-build

WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install
COPY frontend/ ./
RUN npm run build

FROM python:3.12-slim AS app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    SPENDDECK_DATA_DIR=/data

WORKDIR /app

COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

COPY backend/ /app/backend/
COPY catalog/ /app/catalog/
COPY --from=frontend-build /app/frontend/dist /app/frontend/dist

RUN mkdir -p /data && python /app/backend/manage.py collectstatic --noinput

EXPOSE 8000
VOLUME ["/data"]

CMD ["sh", "-c", "python backend/manage.py migrate --noinput && gunicorn --chdir backend config.wsgi:application --bind 0.0.0.0:8000 --workers 2"]
