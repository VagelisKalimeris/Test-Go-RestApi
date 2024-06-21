# Choose base image
FROM python:3.11

# Create dir
WORKDIR /test-go-rest

# Install dependencies
COPY ./requirements.txt /test-go-rest/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /test-go-rest/requirements.txt

# Copy necessary files
COPY . /test-go-rest/


# Run tests
CMD ["/bin/bash","-c","pytest -v"]