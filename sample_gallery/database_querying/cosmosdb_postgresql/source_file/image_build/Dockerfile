# Use the PromptFlow runtime as a parent image
FROM mcr.microsoft.com/azureml/promptflow/promptflow-runtime-stable:latest

# Upgrade pip
RUN python -m pip install --upgrade pip

# Install system packages required for pyodbc
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    unixodbc-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install PostgreSQL ODBC Driver
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    && curl https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - \
    && echo "deb http://apt.postgresql.org/pub/repos/apt/ buster-pgdg main" > /etc/apt/sources.list.d/pgdg.list \
    && apt-get update \
    && apt-get install -y odbc-postgresql \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install required packages defined in requirements.txt
COPY ./* ./
RUN pip install -r requirements.txt