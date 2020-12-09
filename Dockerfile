FROM alpine:3.7
RUN apk update && \
        apk upgrade && \
        apk add --no-cache bash && \
        apk add --no-cache --virtual=build-dependencies unzip \
        && apk add --no-cache curl \
        && apk add --no-cache openjdk8-jre
RUN apk add --no-cache python3 && \
        python3 -m ensurepip && \
         pip3 install --upgrade pip setuptools && \
        rm -r /usr/lib/python*/ensurepip
RUN pip3 install --upgrade pip && \
        pip3 install wheel
RUN apk add --update  python python3 python-dev python3-dev gfortran py-pip build-base
RUN apk update && apk add --no-cache libc6-compat && apk add bash
ADD randomForest_prediction.py /
ADD myRandomModel /myRandomModel
RUN mkdir -p /TestData
RUN pip3 install --upgrade pip
RUN pip3 install pyspark
RUN pip3 install numpy
