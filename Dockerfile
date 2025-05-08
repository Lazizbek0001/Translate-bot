FROM python:3.11-slim

WORKDIR /app

RUN python -m venv venv

RUN /bin/bash -c "source /app/venv/bin/activate && pip install --upgrade pip"

ENV PATH="/app/venv/bin:$PATH"

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "main.py"]
