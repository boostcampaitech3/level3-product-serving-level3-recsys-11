run_server:
	python3 -m Backend

run_client:
	python3 -m streamlit run --server.port 30001 --server.fileWatcherType none Frontend/main.py



run_app: run_server run_client

