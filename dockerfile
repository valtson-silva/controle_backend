FROM python:3.11

WORKDIR /inventory_management

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "inventory_management.wsgi:application"]
