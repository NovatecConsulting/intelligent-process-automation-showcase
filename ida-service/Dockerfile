FROM python:3.9

RUN pip3 install --upgrade pip

# set the working directory in the container
ADD . /code
WORKDIR /code

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip3 install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY src/ .

# Add metadata to the image to describe which port the container is listening on at runtime.
EXPOSE 5000

# command to run on container start
ENTRYPOINT ["python", "./ida_endpoint.py"]
