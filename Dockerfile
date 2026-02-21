FROM python:3.13-slim

# Install system dependencies (needed for psycopg2)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && apt-get clean

# Setup environment variables
ENV PYTHONBUFFERED=1
ENV PORT=8080

# Setup project files and dependencies
WORKDIR /gamer_journey
COPY . /gamer_journey
RUN python -m pip install -r requirements.txt

# Run the application
RUN chmod 755 docker-entry.sh
CMD ["./docker-entry.sh"]
EXPOSE ${PORT}