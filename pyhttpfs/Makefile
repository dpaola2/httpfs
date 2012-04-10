all: python virtualenv

python:
	brew install python
	touch /usr/local/Cellar/python/2.7.2/include/python2.7/osreldate.h

virtualenv:
	virtualenv --no-site-packages --python=/usr/local/Cellar/python/2.7.2/bin/python .

install:
	source bin/activate && pip install -r requirements.txt

clean:
	rm -rf bin lib include build