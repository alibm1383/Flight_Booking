# 1. Use a lightweight Python image
FROM python:3.13-slim

# 2. Prevent Python from writing pyc files and enable live logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Set the working directory inside the container
WORKDIR /workspace

# 4. Copy the requirements file and install dependencies (done early to leverage caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the entire project into the container (folders like venv are ignored via .dockerignore)
COPY . .

# 6. Change to the directory containing main.py and .env
WORKDIR /workspace/Safari_Backend

# 7. Expose port 8000
EXPOSE 8000

# 8. Command to run the project
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]