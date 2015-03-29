cd ../dolittle

# SOURCES
# python -m src.lib.sources.gatd_source -name 'GATD Motion' -out motion -params '{"socketio_host": "gatd.eecs.umich.edu","socketio_port": 8082,"socketio_namespace": "stream","query": {"profile_id": "z9mcJTXvIX"}}'
python -m src.lib.sources.motion_dummy_source -name "Simulated Livingroom Motion Data" -out livingroom/motion &
python -m src.lib.sources.timestamp_seconds_source -name 'Timestamp in Seconds' -out time/timestamps/seconds &

# SINKS
python -m src.lib.sinks.wemo_insight_sink -name 'Big Wall' -in livingroom/lights/cmds:wemo/cmds -params '{"ip_addr": "10.0.0.17"}' &
python -m src.lib.sinks.wemo_insight_sink -name 'Small Wall' -in livingroom/lights/cmds:wemo/cmds -params '{"ip_addr": "10.0.0.229"}' &
python -m src.lib.sinks.wemo_insight_sink -name 'Glass Bubbles' -in livingroom/lights/cmds:wemo/cmds -params '{"ip_addr": "10.0.0.145"}' &
python -m src.lib.sinks.hue_bulb_sink -name 'Lamp' -in livingroom/lights/cmds:livingroom/alerts:hue/lights/cmds -params '{"bridge_addr": "10.0.0.225","bulb_name": "Lamp"}' &
python -m src.lib.sinks.hue_bulb_sink -name 'Fan front' -in livingroom/lights/cmds:hue/lights/cmds -params '{"bridge_addr": "10.0.0.225","bulb_name": "Fan front"}' &
python -m src.lib.sinks.hue_bulb_sink -name 'Fan back' -in livingroom/lights/cmds:hue/lights/cmds -params '{"bridge_addr": "10.0.0.225","bulb_name": "Fan back"}' &
python -m src.lib.sinks.hue_bulb_sink -name 'Fan right' -in livingroom/lights/cmds:hue/lights/cmds -params '{"bridge_addr": "10.0.0.225","bulb_name": "Fan right"}' &
python -m src.lib.sinks.hue_bulb_sink -name 'Fan left' -in livingroom/lights/cmds:hue/lights/cmds -params '{"bridge_addr": "10.0.0.225","bulb_name": "Fan left"}' &

# PROCESSORS
python -m src.lib.processors.motion_timer -name "Livingroom Motion Timer" -in time/timestamps/seconds:livingroom/motion -out livingroom/timers/motion -params '{"duration_secs": 10}' &
python -m src.lib.processors.alert_timer -name "Livingroom Alert Timer" -in time/timestamps/seconds:livingroom/alerts -out livingroom/timers/alert -params '{"duration_secs": 5}' &
python -m src.lib.processors.auto_shutoff -name "Livingroom Autoshutoff" -in livingroom/timers/motion:livingroom/timers/alert -out livingroom/alerts:livingroom/lights/cmds &