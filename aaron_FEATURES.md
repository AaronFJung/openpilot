# Aaron's Fork Features

Everything here is off (or on Default) until you turn it on. Features marked comma four only show as unavailable on a comma 3X. On the comma four, find each one at the bottom of Settings > toggles. In the sunnylink app or website, look under Visuals, except Set Speed Start, which is under Cruise.

## Hide Confidence Ball

Removes the confidence ball from the right edge of the driving screen and lets the camera view stretch into that space. The ball is also the main way the four shows whether sunnypilot is engaged, so with it hidden you lose that cue. comma four only.

## Hide Steering Wheel

Removes the steering wheel icon from the bottom left corner while you drive. It still appears whenever sunnypilot asks you to take control, so you never miss that warning. comma four only.

## Show Planned Stop

When sunnypilot plans to stop for a stop sign, red light or stopped car in the next few seconds, the set speed badge in the top left shows the distance to that stop with STOP underneath, in feet (meters if you use metric). The usual MAX badge still pops up when you change your set speed. It only works while sunnypilot is controlling your gas and brake in experimental mode. It's a heads up, not a promise: keep your foot ready. comma four only.

How it decides (values in `stop_indicator.py`):

* **Plan checked:** the driving model's planned speed and position over its next 10 seconds (33 points).
* **Stop detected:** the first point where planned speed drops below 1.0 m/s (about 2.2 mph, `STOP_SPEED`).
* **Distance shown:** the planned position of that point, rounded to the nearest 10 ft (5 m when metric).
* **Already stopped:** when your own speed is below 0.5 m/s (about 1.1 mph, `MOVING_SPEED`), it shows 0 for as long as the plan keeps you stopped.
* **When it's allowed:** engaged, sunnypilot controlling gas and brake, experimental mode on, and Dynamic Experimental Control either off or in its blended mode.

## Set Speed Start

Chooses what your cruise speed becomes when you press SET. Default keeps the stock behavior, which jumps to 65 mph or higher in experimental mode. My Speed uses your current speed, and My Speed +5 or +10 adds a little on top. It never goes below 25 mph. Only applies when sunnypilot controls gas and brake.

## Torque Bar Height

Makes the curved steering bar at the bottom of the driving screen shorter in height. Default is the normal size. Compact is three quarters as tall and grows only half as much when steering hard. The bar stays the same length.

## Hide Torque Bar

Removes the curved steering bar from the bottom of the driving screen completely. It overrides Torque Bar Height while it's on. comma four only.

## Hide Driver Monitoring Icon

Removes the face icon in the top left that shows where you're looking. Driver monitoring itself keeps running, and its attention warnings and alerts still show and sound exactly as before. comma four only.

## Auto Brightness Offset

Nudges the automatic screen brightness while driving, from 20% darker to 20% brighter in 5% steps. It never goes below 10% or above 100%. It only applies in the Auto brightness modes; the fixed brightness choices and parked brightness are unchanged. In sunnylink it's under Display.
