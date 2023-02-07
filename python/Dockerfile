# start with this baseline
FROM alpine:latest


# upgrade pip3 and install requirements
RUN mkdir build
RUN mkdir /working
RUN mkdir /working/htdocs
COPY . build/
COPY w3gms_sched.py /working
RUN /bin/sh build/install.sh

# run jupyter
WORKDIR /working
CMD ["/working/w3gms_sched.py"]
#CMD /bin/sh -l
