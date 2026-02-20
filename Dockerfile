FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "run.py"]