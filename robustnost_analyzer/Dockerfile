FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt .
# pytest is only needed for development, not inside the add-on
RUN grep -v '^pytest' requirements.txt > /tmp/requirements-addon.txt \
    && pip install --no-cache-dir -r /tmp/requirements-addon.txt

COPY . .

CMD ["python", "-u", "web.py"]
