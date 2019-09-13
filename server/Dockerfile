FROM python:3.7.4
ADD ./server.py /server.py
RUN pip install flask pymongo
CMD ["/usr/bin/env", "python3", "/server.py"]
