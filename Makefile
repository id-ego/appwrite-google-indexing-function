NAME=$(shell basename $(shell pwd))

.PHONY: push git-commit login

push:
	appwrite deploy function

git-commit:
	git add .
	@echo "Enter commit message: "; \
	read MESSAGE; \
	git commit -m "${NAME}: $$MESSAGE"

login:
	@echo "Appwrite Login..."
	appwrite logout; \
	appwrite client --endpoint https://cloud.appwrite.io/v1; \
	appwrite login; \
	appwrite client --debug
