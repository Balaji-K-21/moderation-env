# 1. Use a lightweight version of Python 3.13 as the base
FROM python:3.13-slim

# 2. Define where the code will live inside the container
WORKDIR /app

# 3. Copy the "Shopping List" first to make building faster
COPY requirements.txt .

# 4. Install the libraries (fastapi, openenv-core, etc.)
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy everything else from your folder into the container
COPY . .

# 6. Tell the container to open Port 8000 (where our API lives)
EXPOSE 7860

# 7. The command that starts your server automatically
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]