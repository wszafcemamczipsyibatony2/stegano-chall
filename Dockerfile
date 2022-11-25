FROM ubuntu
RUN apt-get install git
RUN git clone https://github.com/wszafcemamczipsyibatony2/stegano-chall.git
RUN apt-get update && apt-get install -y \
	exiftool \
	python3 \
	python3-pip
RUN pip3 install flask
RUN mkdir /code

RUN cp -a stegano-chall/* /code
WORKDIR /code
RUN chmod 0444 *
RUN ls -al
EXPOSE 5000
CMD ["flask", "run", "--host", "0.0.0.0","--port", "80"]