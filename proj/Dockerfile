FROM python:3.9

COPY . /app

WORKDIR /app

# Install packages
RUN pip install -r requirements.txt

# Run flask app
EXPOSE 5000
# 3 рабочих потока
CMD ["gunicorn", "-w", "3", "-b", ":5000", "-t", "360", "--reload", "src.main:app"] 

