NAME=$(shell basename $(shell pwd))
.PHONY: push git-commit pip-install

push:
	(cd ../.. && appwrite deploy function)

git-commit:
	git add .
	@echo "Enter commit message: "; \
	read MESSAGE; \
	git commit -m "${NAME}: $$MESSAGE"

pip-install:
	pipenv install

requirements:
	pipenv requirements > requirements.txt
