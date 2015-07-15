export PYTHONPATH=/Users/meghan/git_shed/dolittle/dolittle-runtime/lib/blocks


cd ../blocks/sources

# SOURCES
#MOTION python motion_dummy_source.py -name "Simulated Livingroom Motion Data" -out livingroom/motion &
python hue_bulb_source.py -name 'Fan front' -out livingroom/lighting/status -params '{"bridge_addr": "10.0.0.225","bulb_name": "Fan front"}' &
python hue_bulb_source.py -name 'Fan back' -out livingroom/lighting/status -params '{"bridge_addr": "10.0.0.225","bulb_name": "Fan back"}' &
python hue_bulb_source.py -name 'Fan right' -out livingroom/lighting/status -params '{"bridge_addr": "10.0.0.225","bulb_name": "Fan right"}' &
python hue_bulb_source.py -name 'Fan left' -out livingroom/lighting/status -params '{"bridge_addr": "10.0.0.225","bulb_name": "Fan left"}' &
python timestamp_seconds_source.py -name 'Timestamp in Seconds' -out time/timestamps/timestamp_seconds &

cd ../sinks

# SINKS
python gatd_sink.py -name "GATD Dolittle storage" -in time/parts/hour:time/parts/minute:time/parts/second:livingroom/lighting/binary/status:motion/filtered:livingroom/transitions:livingroom/lighting/status:time/timestamps/timestamp_seconds:motion &

cd ../processors

# PROCESSORS
python time_part.py -name "Current hour" -in time/timestamps/timestamp_seconds -out time/parts/hour -params '{"part": "hour"}'
python time_part.py -name "Current minute" -in time/timestamps/timestamp_seconds -out time/parts/minute -params '{"part": "minute"}'
python time_part.py -name "Current second" -in time/timestamps/timestamp_seconds -out time/parts/second -params '{"part": "second"}' &
python binary_lights.py -name "Livingroom binary light status" -in livingroom/lighting/status -out livingroom/lighting/binary/status &
python filter.py -name "Motion from livingroom and adjacent rooms" -in motion -out motion/filtered -params '{"or": [{"": ""}, {"": ""}, {"": ""}, {"": ""}]}' &
python room_enter_exit.py "Enter and exit events for livingroom" -in motion/filtered -out livingroom/transitions &