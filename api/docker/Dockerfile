FROM python:3.8-alpine as base                                                                                  
FROM base as builder                                                                                                          

RUN mkdir /install                                                                                                            
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev libffi-dev openssl-dev make
WORKDIR /install                                                                                                              
COPY requirements.txt /requirements.txt                                                                                       
RUN python3 -m pip install --upgrade pip && python3 -m pip install --prefix=/install -r /requirements.txt                                                     

FROM base                                                                                                                     

COPY --from=builder /install /usr/local                                                                                       
COPY src /project                                                                                                         
RUN apk --no-cache add libpq                                                                                                  
WORKDIR /project
ENTRYPOINT ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "app:app"]
#CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app", "--log-level", "info", "--access-logfile", "-", "--error-logfile", "-"]
