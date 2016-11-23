#!/usr/bin/env python3

from PIL import Image
import cairosvg
import io


# load frame
frame = Image.open('./test-frames/g2x-1479068752-0000.tif', 'r')

# load overlay
overlay_bytes = cairosvg.svg2png(
    url='./test-overlays/g2x-1479068752-0000.svg'
)
overlay = Image.open(io.BytesIO(overlay_bytes))

# create composite image holde
composite = Image.new('RGB', frame.size, (255, 255, 255, 255))

# composite images
composite.paste(frame)
composite.paste(overlay, (0, 0), overlay)

# output result
composite.save('./test-composites/g2x-1479068752-0000.png')
