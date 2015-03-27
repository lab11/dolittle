cd ../dolittle

# SOURCES
python -m src.lib.sources.test_message_source -name "Test Message" -out test -params '{"message": {"type": "turn off"}, "delay_secs": 1}'&
python -m src.lib.sources.test_message_source -name "Test Message" -out test -params '{"message": {"type": "turn on"}, "delay_secs": 2}'&


# SINKS
# put wemo sinks here
python -m src.lib.sinks.wemo_insight_sink -name 'Wemo Minion' -in test -params '{"ip_addr": "10.0.0.17"}' &
