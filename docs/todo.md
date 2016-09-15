# TODO

√ Start/stop preview
  √ Control placement and size of preview
√ Start/stop record
  - Use overlay to indicate if currently recording
	  √ Overlays are not included in the saved video
	  √ We can't use text as that will become part of the saved video
	  - ISSUE: picamera overlays do not honor per-pixel alpha. We may be able to change the overlay mode in the library itself and then use an RGBA file
  √ When recording starts, use a timestamp for the video file
√ Increase/decrease brightness
√ Increase/decrease contrast
√ Change framerate
  - Using 24 fps, but see "Change resolution" below
√ Change resolution
  √ Using 1296x972
  √ RESOLVED: Video is cropped if we use frame rates higher than 15fps. The following posts suggests using 1296x972
    √ https://www.raspberrypi.org/forums/viewtopic.php?f=43&t=137702 (see first response)
    √ https://www.raspberrypi.org/blog/new-camera-mode-released/
√ Allow annotations
  √ These are included in the video recording
- Resize terminal from command-line
  - It looks like the terminal over the serial port is locked in at 80x24

# Possible features
- Change white balance setting?
- Change ISO?
- Consider
	- analog_gain
	- awb_gains
	- color_effects
	- exposure_mode
	- exposure_speed
	- hflip
	- vflip
	- video_denoise
	- video_stabilization
	- image_effect
	- led
	- meter_mode
	- rotation
	- saturation
	- sharpness
	- shutter_speed
