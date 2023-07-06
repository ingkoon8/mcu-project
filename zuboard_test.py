import time 
import numpy as np
from pynq import pl
from pynq import Overlay
from pynq.lib.video import *
import cv2
import matplotlib.pyplot as plt

ol = Overlay('/home/xilinx/jupyter_notebooks/TPG_overlay/tpg.bit')

pixel_in = ol.pixel_pack_2_0
pixel_in.bits_per_pixel = 24

colourspace_in = ol.color_convert_2_0
rgb2bgr = [0.0, 1.0, 0.0,
           1.0, 0.0, 0.0,
           0.0, 0.0, 1.0,
           0.0, 0.0, 0.0]

colourspace_in.colorspace = rgb2bgr

cam_vdma = ol.axi_vdma_0
lines = 512
framemode = VideoMode(640, lines, 24)
cam_vdma.readchannel.mode = framemode
cam_vdma.readchannel.start()

tpg = ol.v_tpg_0
tpg.write(0x10,512)
tpg.write(0x18,640)
tpg.write(0x40,0)
tpg.write(0x30,0)
tpg.write(0x20,0xB)
tpg.write(0x00,0x81)

frame_camera = cam_vdma.readchannel.readframe()
frame_color=cv2.cvtColor(frame_camera,cv2.COLOR_BGR2RGB)
pixels = np.array(frame_color)
plt.imshow(pixels)
plt.show()
