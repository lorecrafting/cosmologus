dev:
	evennia start && evennia --istart --log

watch:
	find ./ -type f -not -path "./server" | entr sh -c 'evennia reload'
