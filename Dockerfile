FROM python:3.9.1

# Create app directory
WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

# Bundle app source
COPY . .

CMD [ "python", "-u", "main.py" ]