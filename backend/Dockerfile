FROM python:3.14-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN mkdir /app/test
COPY test/dpg4x_example2.* /app/test

RUN apt-get update && apt-get install -y \
    mplayer \
    mencoder \
    sox \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

COPY backend /app/backend

# Set the python path to include the current directory so imports work correctly
ENV PYTHONPATH=/app

# Create a non-root user
RUN groupadd -r dpg4x && useradd -r -g dpg4x dpg4x

# Set ownership of the application directory
RUN mkdir -p /app/work && chown -R dpg4x:dpg4x /app

# Switch to non-root user
USER dpg4x

EXPOSE 5000

CMD ["python", "backend/app.py"]
