FROM python:3.7.4
ADD ./fetcher.py /fetcher.py
RUN pip install xmltodict pymongo
CMD ["/usr/bin/env", "python3", "/fetcher.py"]
