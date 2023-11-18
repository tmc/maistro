# This makefile contains the commands to build and run the project.

.PHONY: deps
deps:
	@command -v maestro > /dev/null || (curl -Ls "https://get.maestro.mobile.dev" | bash)

.PHONY: download-samples
download-samples: deps
	@maestro download-samples
