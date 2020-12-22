SHELL := /bin/bash

package:
	zip -r packaged.zip \
		functions \
		cfn-publish.config \
		statemachine \
		-x '**/__pycache*' @

version:
	@echo $(shell cfn-flip template.yaml | python -c 'import sys, json; print(json.load(sys.stdin)["Mappings"]["Solution"]["Constants"]["Version"])')
