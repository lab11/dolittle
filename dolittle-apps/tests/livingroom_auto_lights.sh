export PYTHONPATH=/Users/meghan/git_shed/dolittle/dolittle-runtime/lib/blocks

cd ../processors

# PROCESSORS
python motion_timer.py -name "Livingroom Motion Timer" -in time/timestamps/timestamp_seconds:livingroom/motion -out livingroom/timers/motion_timers -params '{"duration_secs": 10}' &
python alert_timer.py -name "Livingroom Alert Timer" -in time/timestamps/timestamp_seconds:livingroom/alerts -out livingroom/timers/alert_timers -params '{"duration_secs": 5}' &
python auto_shutoff.py -name "Livingroom Autoshutoff" -in livingroom/timers/motion_timers:livingroom/timers/alert_timers -out livingroom/alerts:livingroom/lights/cmds &