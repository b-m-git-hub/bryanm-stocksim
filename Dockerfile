# Using python
FROM python:3.10-slim

# Make and set working directory
RUN mkdir /stock_app
WORKDIR /stock_app

# Using layered approach for installation of requirements
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy files to container
COPY . .

# Expose port
EXPOSE 8050

# Run APP
CMD gunicorn -b 0.0.0.0:${PORT:-8050} app:server