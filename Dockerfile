# Use the official Python base image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /realestate
# Copy the requirements file and install dependencies
COPY requirements.txt /realestate/requirements.txt
RUN pip install -r requirements.txt




# Copy the project files into the container
COPY . /realestate

# Expose the port for Django development server
EXPOSE 8000
CMD ["python", "manage.py", "migrate"]

# Set the command to run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
