FROM python:3.13-slim

# Setup environment variables
ENV PYTHONBUFFERED=1
ENV PORT=8080

# Setup project files and dependencies
WORKDIR /gamer_journey
COPY . /gamer_journey
RUN python -m pip install -r requirements.txt

# Run the application
CMD ["/bin/bash", "-c", "gunicorn gamer_journey.wsgi:application --bind 0.0.0.0:$PORT"]
# CMD gunicorn gamer_journey.wsgi:application --bind 0.0.0.0:${PORT}
EXPOSE ${PORT}