help: ## Prompts help for every command, try `make`
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

slides:  ## Generate the slides
	mdslides slides/effective_testing_master.md
	#mdslides slides/testing_efectivo_master.md
	cp effective_testing_master/index.html ../reveal.js/index.html
	#cp testing_efectivo_master/index.html ../reveal.js/index.html

browser: slides  ## Generate slides and open them in the browser
	xdg-open http://localhost:8000
	@echo "Click 'S' for speakerview"

current-tests:  ## Run tests marked as current
	pytest -m current -s -vv

clean-md:  # #Copy slides to a separate file without extra
	@cp slides/testing_efectivo_master.md slides/testing_efectivo.md
	@cp slides/effective_testing_master.md slides/effective_testing.md
	@sed -i -e "/comment/d" -e "/<\?aside/d" -e "/↓/d" slides/testing_efectivo.md
	@sed -i -e "/comment/d" -e "/<\?aside/d" -e "/↓/d" slides/effective_testing.md
	#sed -i -e "/./b;:n;N;s/\n$//;tn" slides/testing_efectivo.md  , keep the double //

.PHONY: help slides browser current-tests clean-md
