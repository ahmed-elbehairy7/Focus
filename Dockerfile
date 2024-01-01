FROM python:3.7-windowsservercore-1809 

WORKDIR /usr/bin/src

COPY . .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "./focus.io.py"]