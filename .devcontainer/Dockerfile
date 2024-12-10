# Use an official Python base image for Flask development
FROM mcr.microsoft.com/devcontainers/python:3.10

# Set the working directory
WORKDIR /workspace

# Copy the installation script into the container and run it
COPY install.sh /tmp/install.sh
RUN chmod +x /tmp/install.sh && /tmp/install.sh

# Expose Flask's default port
EXPOSE 5000
