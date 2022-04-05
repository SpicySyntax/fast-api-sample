FROM python:3.8-slim

# Install pipev
RUN pip install pipenv

# Copy using Pipfile and Pipfile.lock into image
COPY Pipfile* ./

RUN pipenv sync --system -v

COPY ./app /app/

EXPOSE 80

CMD ["uvicorn","app.main:app", "--host", "0.0.0.0", "--port", "80", "--workers", "2"]