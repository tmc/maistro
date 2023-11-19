.PHONY: build
build: deps
	nx run maistro:build:development

.PHONY: deps
deps:
	@command -v nx >/dev/null 2>&1 || { echo >&2 "I require nx but it's not installed."; npm install -g nx; }

