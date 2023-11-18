# This makefile contains the commands to build and run the project.

.PHONY: deps
deps:
	@command -v maestro > /dev/null || (curl -Ls "https://get.maestro.mobile.dev" | bash)

.PHONY: download-samples
download-samples: deps
	@maestro download-samples

.PHONY: run-sample-flow
run-sample-flow:
	cd ./samples
	unzip sample.zip
	xcrun simctl install Booted Wikipedia.app
	maestro test ios-flow.yaml
