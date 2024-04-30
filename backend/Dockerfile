FROM python:3.9-slim
WORKDIR /
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . ./
EXPOSE 8000
CMD ["python3", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]