# FROM python:3.8-alpine as base                                                                                  
# # FROM base as builder                                                                                                          

# RUN mkdir /install                                                                                                            
# RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev libffi-dev openssl-dev make                                                                                                              
# COPY requirements.txt /requirements.txt                                                                                       
# RUN python3 -m pip install --upgrade pip && python3 -m pip install --prefix=/install -r /requirements.txt                                                     

# FROM base                                                                                                                     

# COPY --from=builder /install /usr/local                                                                                       
# COPY src /project                                                                                                         
# RUN apk --no-cache add libpq                                                                                                  
# WORKDIR /project
# ENTRYPOINT ["uvicorn", "--host", "0.0.0.0", "--port", "8080", "app:app"]
# #CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app", "--log-level", "info", "--access-logfile", "-", "--error-logfile", "-"]
# FROM python:3.11-rc-alpine3.15
FROM python:3.11-rc


ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.0.0

# System deps:
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
WORKDIR /code
COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml

# Project initialization:
RUN poetry config virtualenvs.create false
RUN ls
RUN poetry install

# Creating folders, and files for a project:
# COPY . /code