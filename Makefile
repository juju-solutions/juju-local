PY := venv/bin/python
# If the bin version does not exist look in venv/local/bin
ifeq ($(wildcard venv/bin/pip),)
  PIP = venv/local/bin/pip
else
  PIP = venv/bin/pip
endif
# If the bin version does not exist look in venv/local/bin
ifeq ($(wildcard venv/bin/flake8),)
  FLAKE = venv/local/bin/flake8
else
  FLAKE = venv/bin/flake8
endif
# If the bin version does not exist look in venv/local/bin
ifeq ($(wildcard venv/bin/nosetests),)
  NOSE = venv/local/bin/nosetests
else
  NOSE = venv/bin/nosetests
endif

# ###########
# Build
# ###########

.PHONY: install
install: venv develop

venv: $(PY)
$(PY):
	python3 -m venv --without-pip venv
	curl https://bootstrap.pypa.io/ez_setup.py | $(PY)
	venv/bin/easy_install pip || venv/local/bin/easy_install pip
	rm setuptools*.zip

.PHONY: clean_all
clean_all: clean clean_venv

.PHONY: clean_venv
clean_venv:
	rm -rf venv

.PHONY: clean
clean:
	find . -name '*.pyc' -delete
	find . -name '*.bak' -delete
	find . -name __pycache__ -delete
	rm -f .coverage

develop: lib/python*/site-packages/juju_local.egg-link
lib/python*/site-packages/juju_local.egg-link:
	$(PIP) install --find-links=reqs jujuclient
	$(PY) setup.py develop

.PHONY: sysdeps
sysdeps:
	sudo apt-get $(shell tty -s || echo -y) install python3-dev juju-core bzr python3-setuptools

# ###########
# Develop
# ###########

$(NOSE): $(PY)
	$(PIP) install -r test-requires.txt

.PHONY: test
test: $(NOSE)
	make py3test

.PHONY: unit_test
unit_test: $(NOSE)
	make ARGS="-e functional" py3test

.PHONY: functional_test
functional_test: $(NOSE)
	make ARGS="tests/functional" py3test

# This is a private target used to get around finding nose in different paths.
# Do not call this manually, just use make test.
.PHONY: py3test
py3test:
	@echo Testing Python 3...
	@$(NOSE) --nologcapture $(ARGS)

.PHONY: coverage
coverage: $(NOSE)
	@echo Testing with coverage...
	@$(NOSE) --nologcapture --with-coverage --cover-package=jujulocal

.PHONY: lint
lint:
	@find $(sources) -type f \( -iname '*.py' ! -iname '__init__.py' ! -iwholename '*venv/*' \) -print0 | xargs -r0 $(FLAKE)

.PHONY: check
check: test lint

.PHONY: all
all: clean venv coverage lint


# ###########
# Deploy
# ###########
.PHONY: dist
dist:
	$(PY) setup.py sdist

.PHONY: upload
upload:
	$(PY) setup.py sdist upload

.PHONY: version_update
version_update:
	$(EDITOR) setup.py
