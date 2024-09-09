# Animations

The GUI can play animations of the scene.

## Animations with fixed length

Animations with a fixed length can be started using the `animation_start` method of main.

All information required for the animation is given as input to the method.
This method takes the DOFs for the animation as well as the time as input.

When the animation is terminated or finished then the DOFs are restored to a given final value.

### user interaction

If `show_animation_bar` is true then the user can interact with the animation using the trackbar and play/pause/stop buttons.

### Uses

- Mode shape visualization (as loop)
- Airy wave response (as loop)
- Movement to new equilibrium (as single animation without user control)

## Animations with unlimited length

Animations with an unknown length (time domain simulations, time-domain realizations of frequency domain results)
can be started using the `animation_start_external_control` method of main.

User controls are provided by the GUI and allow the user to do the following:
- change the current time of the animation (slider)
- pause/continue the animation
- extend the end-time of the animation (the right end of the slider)
- stop the animation

The end-time is automatically extended when the animation reaches the current end-time.
The time is the real-time in seconds by default, but can be changed by the user.

The information required for the animation is obtained when needed using a callback function.

- callback new_time_activated ( t, viewport ) -> DOFs
- callback request stop -> final dofs
- callback request  
- callback endtime_changed -> new endtime

## Timing

The animation is played in real-time by default.
The user can set the time scaling factor to speed up or slow down the animation.

To keep track of the animation time, the system time is used.
The time is updated every frame and the time difference is used to calculate the new time.

So we store:
_animation_last_frame_animation_time 
_animation_last_frame_clock_time (time.time())


