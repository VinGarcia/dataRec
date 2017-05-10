
run:
	@printf 'Please inform the json argument file (e.g. js_model.json): '
	@read a && sudo python main.py $$a
