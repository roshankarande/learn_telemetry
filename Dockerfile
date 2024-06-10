# 
FROM python:3.12

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN opentelemetry-bootstrap -a install
# 
COPY ./app /code/app

# 
# CMD ["opentelemetry-instrument","--traces_exporter","console","--metrics_exporter","console","--logs_exporter","console","--service_name","sample-app-rk"  "fastapi", "run", "app/main.py", "--port", "5001"]
# CMD ["opentelemetry-instrument","--traces_exporter","console","--metrics_exporter","console","--logs_exporter","console","--service_name","sample-app-rk"  "fastapi", "run", "app/main.py", "--port", "5001"]
# CMD ["opentelemetry-instrument","--traces_exporter","console","fastapi", "run", "app/main.py", "--port", "5001"]
# CMD ["opentelemetry-instrument","--traces_exporter","otlp","fastapi", "run", "app/main.py", "--port", "5001"]
CMD ["opentelemetry-instrument","fastapi", "run", "app/main.py", "--port", "5001"]
# CMD ["python", "app/simple.py"]