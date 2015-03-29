cd ../dolittle

# Hues
python -m src.lib.sources.hue_bulb_source -name 'Lamp' -out livingroom/lights:hue/lights -params '{"bridge_addr": "10.0.0.225","bulb_name": "Lamp"}' &
python -m src.lib.sources.hue_bulb_source -name 'Fan front' -out livingroom/lights:hue/lights -params '{"bridge_addr": "10.0.0.225","bulb_name": "Fan front"}' &
python -m src.lib.sources.hue_bulb_source -name 'Fan back' -out livingroom/lights:hue/lights -params '{"bridge_addr": "10.0.0.225","bulb_name": "Fan back"}' &
python -m src.lib.sources.hue_bulb_source -name 'Fan right' -out livingroom/lights:hue/lights -params '{"bridge_addr": "10.0.0.225","bulb_name": "Fan right"}' &
python -m src.lib.sources.hue_bulb_source -name 'Fan left' -out livingroom/lights:hue/lights -params '{"bridge_addr": "10.0.0.225","bulb_name": "Fan left"}' &
python -m src.lib.sources.hue_bulb_source -name 'Kitchen' -out livingroom/lights:hue/lights -params '{"bridge_addr": "10.0.0.225","bulb_name": "Kitchen"}' &

# Wemos
python -m src.lib.sources.wemo_insight_source -name 'Glass Bubble Lights' -out livingroom/lights:livingroom/wemo:wemo -params '{"ip_addr": "10.0.0.145", "device_name": "Bumblebee"}' &
python -m src.lib.sources.wemo_insight_source -name 'Big Wall Lights' -out livingroom/lights:livingroom/wemo:wemo -params '{"ip_addr": "10.0.0.17", "device_name": "Flea"}' &
python -m src.lib.sources.wemo_insight_source -name 'Tea House Lights' -out livingroom/lights:livingroom/wemo:wemo -params '{"ip_addr": "10.0.0.229", "device_name": "Caterpillar"}' &