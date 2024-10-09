all:
	python3 scripts/data_fetch_and_process.py
	python3 scripts/convert_to_final_data.py

clean:
	rm -rf data/* /archive/*

.PHONY: clean