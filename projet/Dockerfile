FROM python:3.11
RUN pip3 install fastapi uvicorn tortoise-orm
COPY ./app /app
CMD [ "uvicorn", "app.main:mountain_peak_app", "--host", "0.0.0.0", "--port", "11000"]