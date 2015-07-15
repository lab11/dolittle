export PYTHONPATH=/home/daniel/dolittle/dolittle-runtime/lib/blocks

cd ../blocks/sources

# SOURCES

# External
 python socket_source.py -name "JSON Input Client" -out ghosting/in -params '{"host": "localhost", "port": 7774}' &

# Living Room
#python hue_bulb_source.py -name 'livingroom1' -out livingroom/lights/status -params '{"bridge_addr": "192.168.1.4","bulb_name": "livingroom1"}' &
#python hue_bulb_source.py -name 'livingroom2' -out livingroom/lights/status -params '{"bridge_addr": "192.168.1.4","bulb_name": "livingroom2"}' &

# Bedroom
python hue_bulb_source.py -name 'bedroom1' -out bedroom/lights/status -params '{"bridge_addr": "192.168.1.4","bulb_name": "bedroom1"}' &
#python hue_bulb_source.py -name 'bedroom2' -out bedroom/lights/status -params '{"bridge_addr": "192.168.1.4","bulb_name": "bedroom2"}' &

# Bathroom
#python hue_bulb_source.py -name 'bathroom1' -out bathroom/lights/status -params '{"bridge_addr": "192.168.1.4","bulb_name": "bathroom1"}' &

# Kitchen
#python hue_bulb_source.py -name 'kitchen1' -out kitchen/lights/status -params '{"bridge_addr": "192.168.1.4","bulb_name": "kitchen1"}' &

cd ../processors

# PROCESSORS
python ghosting_app.py -name "Daniel Ghosting" -in livingroom/lights/status:bedroom/lights/status:ghosting/in -out ghosting/out:livingroom/lights/cmds:bedroom/lights/cmds:bathroom/lights/cmds:kitchen/lights/cmds

cd ../sinks

# External
python socket_sink.py -name "JSON Output Client" -in ghosting/out -params '{"dest": "107.4.83.157", "port": 8080}' &

# Living Room
#python hue_bulb_sink.py -name 'livingroom1' -in livingroom/lights/cmds -params '{"bridge_addr": "192.168.1.4","bulb_name": "livingroom1"}' &
#python hue_bulb_sink.py -name 'livingroom2' -in livingroom/lights/cmds -params '{"bridge_addr": "192.168.1.4","bulb_name": "livingroom2"}' &

# Bedroom
python hue_bulb_sink.py -name 'bedroom1' -in bedroom/lights/cmds -params '{"bridge_addr": "192.168.1.4","bulb_name": "bedroom1"}' &
#python hue_bulb_sink.py -name 'bedroom2' -in bedroom/lights/cmds -params '{"bridge_addr": "192.168.1.4","bulb_name": "bedroom2"}' &

# Bathroom
#python hue_bulb_sink.py -name 'bathroom1' -in bathroom/lights/cmds -params '{"bridge_addr": "192.168.1.4","bulb_name": "bathroom1"}' &

# Kitchen
#python hue_bulb_sink.py -name 'kitchen1' -in kitchen/lights/cmds -params '{"bridge_addr": "192.168.1.4","bulb_name": "kitchen1"}' &

