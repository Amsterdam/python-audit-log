.PHONY: release dist build test coverage clean distclean


PYTHON = python3
dc = docker-compose
run = $(dc) run --rm

help:                           ## Show this help.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

release: clean-dist build-package build test dist        ## Test, create a distribution and upload it to pypi
	twine upload dist/*

dist:                           ## Create a distribution
	$(PYTHON) setup.py sdist bdist_wheel

build-package:                  ## Build the package
	$(PYTHON) setup.py build

clean-dist:                     ## Delete everything in dist/*
	rm -rf dist/*

build:                          ## Build docker image
	$(dc) build

clean:                          ## Clean docker stuff
	$(dc) down -v --remove-orphans

bash:                           ## Run the container and start bash
	$(run) dev bash

test:                           ## Execute tests
	$(run) test $(ARGS)

prepare_major:                  ## Prepare major release: add changes to Changelog.md, bump version, commit and coverage
	./prepare_release.sh major

prepare_minor:                  ## Prepare minor release: add changes to Changelog.md, bump version, commit and coverage
	./prepare_release.sh minor

prepare_patch:                  ## Prepare patch release: add changes to Changelog.md, bump version, commit and coverage
	./prepare_release.sh patch
