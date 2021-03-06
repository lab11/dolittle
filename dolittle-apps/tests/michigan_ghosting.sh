export PYTHONPATH=/Users/meghan/git_shed/dolittle/dolittle-runtime/lib/blocks

cd ../blocks/sources

# SOURCES

# External
#python socket_source.py -name "JSON Input Client" -out ghosting/in -params '{"host": "10.0.0.239", "port": 8080}' &

# Living Room
#python hue_bulb_source.py -name 'Lamp' -out livingroom/lights/status -params '{"bridge_addr": "10.0.0.225","bulb_name": "Lamp"}' &
#python hue_bulb_source.py -name 'Fan front' -out livingroom/lights/status -params '{"bridge_addr": "10.0.0.225","bulb_name": "Fan front"}' &
#python hue_bulb_source.py -name 'Fan back' -out livingroom/lights/status -params '{"bridge_addr": "10.0.0.225","bulb_name": "Fan back"}' &
#python hue_bulb_source.py -name 'Fan right' -out livingroom/lights/status -params '{"bridge_addr": "10.0.0.225","bulb_name": "Fan right"}' &
#python hue_bulb_source.py -name 'Fan left' -out livingroom/lights/status -params '{"bridge_addr": "10.0.0.225","bulb_name": "Fan left"}' &
#python wemo_insight_source.py -name 'LR Xmas 1' -out livingroom/lights/status -params '{"ip_addr": "10.0.0.17"}' &
#python wemo_insight_source.py -name 'LR Xmas 2' -out livingroom/lights/status -params '{"ip_addr": "10.0.0.145"}' &
#python wemo_insight_source.py -name 'LR Xmas 3' -out livingroom/lights/status -params '{"ip_addr": "10.0.0.229"}' &

# Bedroom
python lifx_source.py -name 'Lotus Lamp' -out bedroom/lights/status -params '{"mac_addr": "d0:73:d5:00:70:36","ip_addr": "10.0.0.104"}' & 
python lifx_source.py -name 'Closet' -out bedroom/lights/status -params '{"mac_addr": "d0:73:d5:02:6c:ea","ip_addr": "10.0.0.115"}' &
python wemo_insight_source.py -name 'Bedroom Xmas' -out bedroom/lights/status -params '{"ip_addr": "10.0.0.53"}' &
python wemo_insight_source.py -name 'Bathroom Xmas' -out bedroom/lights/status -params '{"ip_addr": "10.0.0.38"}' &

# Bathroom
python hue_bulb_source.py -name 'Bathroom' -out bathroom/lights/status -params '{"bridge_addr": "10.0.0.225","bulb_name": "Bathroom"}' &

# Kitchen
#python hue_bulb_source.py -name 'Kitchen 1a' -out kitchen/lights/status -params '{"bridge_addr": "10.0.0.225","bulb_name": "Kitchen 1a"}' &
#python hue_bulb_source.py -name 'Kitchen 1b' -out kitchen/lights/status -params '{"bridge_addr": "10.0.0.225","bulb_name": "Kitchen 1b"}' &
#python hue_bulb_source.py -name 'Kitchen 2a' -out kitchen/lights/status -params '{"bridge_addr": "10.0.0.225","bulb_name": "Kitchen 2a"}' &
#python hue_bulb_source.py -name 'Kitchen 2b' -out kitchen/lights/status -params '{"bridge_addr": "10.0.0.225","bulb_name": "Kitchen 2b"}' &


cd ../processors

# PROCESSORS
# NOT DONE
# python ghosting_app.py -name "Meghan Ghosting" -in livingroom/lights/status:bedroom/lights/status:ghosting/in -out ghosting/out:livingroom/lights/cmds:bedroom/lights/cmds
#python ghosting_app.py -name "Meghan Ghosting" -in livingroom/lights/status:bedroom/lights/status:ghosting/in -out ghosting/out:livingroom/lights/cmds:bedroom/lights/cmds # TEST

cd ../sinks

# External
#python socket_sink.py -name "JSON Output Client" -in ghosting/out -params '{"dest": "70.110.28.225", "port": 7774}' &

# Living Room
#python hue_bulb_sink.py -name 'Lamp' -in livingroom/lights/cmds -params '{"bridge_addr": "10.0.0.225","bulb_name": "Lamp"}' &
#python hue_bulb_sink.py -name 'Fan front' -in livingroom/lights/cmds -params '{"bridge_addr": "10.0.0.225","bulb_name": "Fan front"}' &
#python hue_bulb_sink.py -name 'Fan back' -in livingroom/lights/cmds -params '{"bridge_addr": "10.0.0.225","bulb_name": "Fan back"}' &
#python hue_bulb_sink.py -name 'Fan right' -in livingroom/lights/cmds -params '{"bridge_addr": "10.0.0.225","bulb_name": "Fan right"}' &
#python hue_bulb_sink.py -name 'Fan left' -in livingroom/lights/cmds -params '{"bridge_addr": "10.0.0.225","bulb_name": "Fan left"}' &
#python wemo_insight_sink.py -name 'LR Xmas 1' -in livingroom/lights/cmds -params '{"ip_addr": "10.0.0.17"}' &
#python wemo_insight_sink.py -name 'LR Xmas 2' -in livingroom/lights/cmds -params '{"ip_addr": "10.0.0.145"}' &
#python wemo_insight_sink.py -name 'LR Xmas 3' -in livingroom/lights/cmds -params '{"ip_addr": "10.0.0.229"}' &

# Bedroom
python lifx_sink.py -name 'Lotus Lamp' -in bedroom/lights/cmds -params '{"mac_addr": "d0:73:d5:00:70:36","ip_addr": "10.0.0.104"}' &
python lifx_sink.py -name 'Closet' -in bedroom/lights/cmds -params '{"mac_addr": "d0:73:d5:02:6c:ea","ip_addr": "10.0.0.115"}' &
python wemo_insight_sink.py -name 'Bedroom Xmas' -in bedroom/lights/cmds -params '{"ip_addr": "10.0.0.53"}' & # 53 or 38
python wemo_insight_sink.py -name 'Bathroom Xmas' -in bedroom/lights/cmds -params '{"ip_addr": "10.0.0.38"}' &

# Bathroom
python hue_bulb_sink.py -name 'Bathroom' -in bathroom/lights/cmds -params '{"bridge_addr": "10.0.0.225","bulb_name": "Bathroom"}' &

# Kitchen
#python hue_bulb_sink.py -name 'Kitchen 1a' -in kitchen/lights/cmds -params '{"bridge_addr": "10.0.0.225","bulb_name": "Kitchen 1a"}' &
#python hue_bulb_sink.py -name 'Kitchen 1b' -in kitchen/lights/cmds -params '{"bridge_addr": "10.0.0.225","bulb_name": "Kitchen 1b"}' &
#python hue_bulb_sink.py -name 'Kitchen 2a' -in kitchen/lights/cmds -params '{"bridge_addr": "10.0.0.225","bulb_name": "Kitchen 2a"}' &
#python hue_bulb_sink.py -name 'Kitchen 2b' -in kitchen/lights/cmds -params '{"bridge_addr": "10.0.0.225","bulb_name": "Kitchen 2b"}' &






