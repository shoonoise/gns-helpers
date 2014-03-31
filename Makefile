all:
	true

pylint:
	pypy3 `which pylint` --rcfile=pylint.ini \
		base \
		--output-format=colorized 2>&1 | less -SR

