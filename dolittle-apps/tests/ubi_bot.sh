export PYTHONPATH=/Users/meghan/git_shed/dolittle/dolittle-runtime/lib/blocks

cd ../blocks/sources

# SOURCES
python http_source.py -name "HTTP Portal" -out http:http/ubi:http/motion:http/chat -params '{"host": "10.0.0.239", "port": 80}'&

cd ../sinks

# SINKS
python chatbot_sink.py -name "ALICE Chatbot" -in http/chat -params '{"chatbot_path": "/Users/meghan/lib/pyaiml"}'&