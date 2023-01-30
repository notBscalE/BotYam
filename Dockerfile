FROM python:latest
COPY . /etc/botyam
WORKDIR /etc/botyam
RUN pip install -r requirements.txt
CMD ["python3", "-u ./src/main.py"]