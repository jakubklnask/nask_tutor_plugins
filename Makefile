.PHONY: install-plugins enable-plugins setup-plugins

install-plugins:
	tutor plugins install mfe
	@for plugin in *.py; do \
		tutor plugins install $$plugin; \
	done

enable-plugins:
	tutor plugins enable mfe
	@for plugin in *.py; do \
		name=$$(basename $$plugin .py); \
		tutor plugins enable $$name; \
	done

setup-plugins: install-plugins enable-plugins
	tutor plugins install aspects
	tutor plugins disable indigo
	@echo "All plugins installed and enabled"
