FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt /app/

#Instal all packages from requirmenets file
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . /app

# Expose Streamlit’s default port
EXPOSE 8501

# Command to run the Streamlit app
CMD ["streamlit", "run", "main.py", "--server.runOnSave", "true"]


