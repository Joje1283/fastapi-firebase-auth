FROM python:3.10.11
ARG YOUR_ENV
ENV YOUR_ENV=${YOUR_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.7.1

# System deps:
RUN pip install --upgrade pip
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to redis them in docker layer
WORKDIR /code
COPY poetry.lock pyproject.toml /code/

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install $(test "$YOUR_ENV" == production && echo "--no-dev") --no-interaction --no-ansi --no-dev

# Creating folders, and files for a project:
COPY . /code
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "main:app"]

# test run command
# docker build -t test_build . --platform linux/amd64
# docker run -it --rm -p 8000:8000 test_build