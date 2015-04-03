export PYTHONPATH=/Users/meghan/git_shed/dolittle/dolittle-runtime/lib/blocks:$PYTHONPATH

cd ../blocks/sources

# SOURCES
# python -m src.lib.sources.gatd_source -name 'GATD Motion' -out motion -params '{"socketio_host": "gatd.eecs.umich.edu","socketio_port": 8082,"socketio_namespace": "stream","query": {"profile_id": "z9mcJTXvIX"}}'
python motion_dummy_source.py -name "Simulated Livingroom Motion Data" -out livingroom/motion &
python timestamp_seconds_source.py -name 'Timestamp in Seconds' -out time/timestamps/timestamp_seconds &

cd ../sinks

# SINKS
python wemo_insight_sink.py -name 'Big Wall' -in livingroom/lights/cmds:wemo/cmds -params '{"ip_addr": "10.0.0.17"}' &
python wemo_insight_sink.py -name 'Small Wall' -in livingroom/lights/cmds:wemo/cmds -params '{"ip_addr": "10.0.0.229"}' &
python wemo_insight_sink.py -name 'Glass Bubbles' -in livingroom/lights/cmds:wemo/cmds -params '{"ip_addr": "10.0.0.145"}' &
python hue_bulb_sink.py -name 'Lamp' -in livingroom/lights/cmds:livingroom/alerts:hue/lights/cmds -params '{"bridge_addr": "10.0.0.225","bulb_name": "Lamp"}' &
python hue_bulb_sink.py -name 'Fan front' -in livingroom/lights/cmds:hue/lights/cmds -params '{"bridge_addr": "10.0.0.225","bulb_name": "Fan front"}' &
python hue_bulb_sink.py -name 'Fan back' -in livingroom/lights/cmds:hue/lights/cmds -params '{"bridge_addr": "10.0.0.225","bulb_name": "Fan back"}' &
python hue_bulb_sink.py -name 'Fan right' -in livingroom/lights/cmds:hue/lights/cmds -params '{"bridge_addr": "10.0.0.225","bulb_name": "Fan right"}' &
python hue_bulb_sink.py -name 'Fan left' -in livingroom/lights/cmds:hue/lights/cmds -params '{"bridge_addr": "10.0.0.225","bulb_name": "Fan left"}' &

cd ../processors

# PROCESSORS
python motion_timer.py -name "Livingroom Motion Timer" -in time/timestamps/timestamp_seconds:livingroom/motion -out livingroom/timers/motion_timers -params '{"duration_secs": 10}' &
python alert_timer.py -name "Livingroom Alert Timer" -in time/timestamps/timestamp_seconds:livingroom/alerts -out livingroom/timers/alert_timers -params '{"duration_secs": 5}' &
python auto_shutoff.py -name "Livingroom Autoshutoff" -in livingroom/timers/motion_timers:livingroom/timers/alert_timers -out livingroom/alerts:livingroom/lights/cmds &