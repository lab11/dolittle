export PYTHONPATH=/Users/meghan/git_shed/dolittle/dolittle-runtime/lib/blocks

cd ../blocks/sources

# SOURCES
python motion_dummy_source.py -name "Simulated Livingroom Motion Data" -out livingroom/motion &
python timestamp_seconds_source.py -name 'Timestamp in Seconds' -out time/timestamps/timestamp_seconds &

cd ../sinks

# SINKS
python wemo_insight_sink.py -name 'Big Wall' -in livingroom/lights/cmds:wemo/cmds -params '{"ip_addr": "10.0.0.17"}' &
python wemo_insight_sink.py -name 'Small Wall' -in livingroom/lights/cmds:wemo/cmds -params '{"ip_addr": "10.0.0.229"}' &
python wemo_insight_sink.py -name 'Glass Bubbles' -in livingroom/lights/cmds:wemo/cmds -params '{"ip_addr": "10.0.0.145"}' &
python hue_bulb_sink.py -name 'Lamp' -in livingroom/lights/cmds:livingroom/alerts:hue/cmds -params '{"bridge_addr": "10.0.0.225","bulb_name": "Lamp"}' &
python hue_bulb_sink.py -name 'Fan front' -in livingroom/lights/cmds:hue/cmds -params '{"bridge_addr": "10.0.0.225","bulb_name": "Fan front"}' &
python hue_bulb_sink.py -name 'Fan back' -in livingroom/lights/cmds:hue/cmds -params '{"bridge_addr": "10.0.0.225","bulb_name": "Fan back"}' &
python hue_bulb_sink.py -name 'Fan right' -in livingroom/lights/cmds:hue/cmds -params '{"bridge_addr": "10.0.0.225","bulb_name": "Fan right"}' &
python hue_bulb_sink.py -name 'Fan left' -in livingroom/lights/cmds:hue/cmds -params '{"bridge_addr": "10.0.0.225","bulb_name": "Fan left"}' &