# Docker command to use, can be podman
ifneq (, $(shell which podman))
CONTAINER_RUNTIME := podman
else
ifneq (, $(shell which docker))
CONTAINER_RUNTIME := docker
else
$(error "Neither docker nor podman are available in PATH")
endif
endif

LATEST_TAG := $(shell git describe --tags `git rev-list --tags --max-count=1`)
SHORT_HASH := $(shell git rev-parse --short HEAD)

IMG_TAG ?= ${LATEST_TAG}-${SHORT_HASH}
IMG ?= quay.io/yblum/knowledge_base_gpt:${IMG_TAG}

# By default build for Linux on x86_64
PLATFORM ?= linux/amd64

.PHONY: image-build
image-build: ## Build the container image.
	$(CONTAINER_RUNTIME) image build --platform ${PLATFORM} -t ${IMG} .

.PHONY: image-push
image-push: ## Push the container image.
	$(CONTAINER_RUNTIME) image push ${IMG}
