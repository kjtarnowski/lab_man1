# pull official base image
FROM python:3.8-slim-buster

# set work directory
WORKDIR /usr/src/lab_man1

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV RDBASE /opt/rdkit-Release_2020_09_2
ENV LD_LIBRARY_PATH $RDBASE/lib:$LD_LIBRARY_PATH
ENV PYTHONPATH=$RDBASE:$PYTHONPATH

# install dependencies
RUN apt-get -y update
RUN apt-get -y install wget flex bison build-essential python-numpy cmake python-dev sqlite3 libsqlite3-dev libboost-all-dev libcairo2-dev libpq-dev gcc musl-dev netcat freetype*  
RUN  wget https://github.com/rdkit/rdkit/archive/Release_2020_09_2.tar.gz
RUN tar xvzf Release_2020_09_2.tar.gz --directory /opt
RUN rm -f xvzf rdkit-Release_2020_09_2.tar.gz
RUN cd  $RDBASE &&  mkdir build && cd build && cmake ..   && make && make install  # -DRDK_BUILD_CAIRO_SUPPORT=ON

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt


# copy entrypoint.sh
COPY ./entrypoint.sh .

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/lab_man1/entrypoint.sh"]
