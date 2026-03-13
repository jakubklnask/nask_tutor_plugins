.PHONY: install-plugins enable-plugins setup-plugins

install-plugins:
	tutor plugins install mfe
	@for plugin in $$(ls *.py 2>/dev/null); do \
		if [ -f "$$plugin" ]; then \
			tutor plugins install $$plugin; \
		fi \
	done

enable-plugins:
	tutor plugins enable mfe
	@for plugin in $$(ls *.py 2>/dev/null); do \
		if [ -f "$$plugin" ]; then \
			name=$$(basename $$plugin .py); \
			tutor plugins enable $$name; \
		fi \
	done

setup-plugins: install-plugins enable-plugins
	tutor plugins install aspects
	tutor plugins enable aspects
	tutor plugins disable indigo
	@echo "All plugins installed and enabled"
