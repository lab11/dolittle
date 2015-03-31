export PYTHONPATH=/Users/meghan/git_shed/dolittle/dolittle-runtime/lib/blocks

cd ../blocks

cd sources
# SOURCES
#python test_message_source.py -name "Test Message" -out test/1 -params '{"message": {"type": "turn off"}, "delay_secs": 1}'
python http_source.py -name "Test Server" -out http:http/ubi:http/motion -params '{"host": "10.0.0.239", "port": 8080}'

cd ../sinks
# SINKS
#python -m src.lib.sinks.wemo_insight_sink -name 'Wemo Minion' -in test -params '{"ip_addr": "10.0.0.17"}' &
