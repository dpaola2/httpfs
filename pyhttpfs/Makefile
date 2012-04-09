all: virtualenv

virtualenv:
	virtualenv --no-site-packages .

install:
	source bin/activate && pip install -r requirements.txt

clean:
	rm -rf bin lib include