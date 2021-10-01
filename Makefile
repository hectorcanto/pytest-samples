slides:  ## Generate the slides
	mdslides slides/effective_testing.md
	mdslides slides/testing_efectivo.md
	cp effective_testing/index.html ../reveal.js/index.html


browser: slides  # Generate slides and open them in browser
	xdg-open ../reveal.js/index.html

current-tests:
	pytest -m current -s -vv

.PHONY: slides browser current-tests
