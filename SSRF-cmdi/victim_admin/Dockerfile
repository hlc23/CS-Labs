FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN apt-get update \
	&& apt-get install -y --no-install-recommends iputils-ping \
	&& rm -rf /var/lib/apt/lists/* \
	&& pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5001
CMD ["python", "app.py"]
