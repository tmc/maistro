# This makefile contains the commands to build and run the project.

.PHONY: deps
deps: ## Install dependencies
	@command -v maestro > /dev/null || (curl -Ls "https://get.maestro.mobile.dev" | bash)
	@command -v xcrun > /dev/null || (xcode-select --install)
	@xcrun simctl list > /dev/null || (sudo xcode-select -s /Applications/Xcode.app)

.PHONY: download-samples
download-samples: deps ## Download samples
	@maestro download-samples

.PHONY: run-sample-flow
run-sample-flow: download-samples ## Run sample flow
	@./scripts/run-sample-flow.sh


venv: requirements.in ## Create virtual environment
	@python3 -m venv venv
	./venv/bin/pip install wheel pip-tools
	./venv/bin/pip-compile requirements.in
	./venv/bin/pip-sync

