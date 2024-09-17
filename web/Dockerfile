FROM python:3
ENV PYTHONUNBUFFERD=1
WORKDIR /app
COPY requirement.txt ./
RUN pip install -r requirement.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--reload"]