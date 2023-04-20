dev:
	evennia start && evennia --istart --log

watch:
	find ./commands ./typeclasses ./world ./web -type f | entr sh -c 'evennia reload'
