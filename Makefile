.PHONY: install-plugins enable-plugins setup-plugins

install-plugins:
	tutor plugins install mfe
	tutor plugins install aspects
	@for plugin in *.py; do \
		tutor plugins install $$plugin; \
	done

enable-plugins:
	tutor plugins enable mfe
	tutor plugins enable aspects
	@for plugin in *.py; do \
		name=$$(basename $$plugin .py); \
		tutor plugins enable $$name; \
	done

setup-plugins: install-plugins enable-plugins
	@echo "All plugins installed and enabled"
