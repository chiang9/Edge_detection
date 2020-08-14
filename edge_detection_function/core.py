import argparse
import cv2 as cv
import numpy as np
from edge_detection_function.tensorflow_layer import CropLayer



class HED_Network(object):

    def __init__(self,protoTxt,mdl):
        super().__init__()
        self.protoTxt = protoTxt
        self.pretrainMdl = mdl
        cv.dnn_registerLayer('Crop', CropLayer)
        self.net = cv.dnn.readNet(self.protoTxt, self.pretrainMdl)
    

    def edge_detection(self,stream,detail_scale,outputSize):
        cap = cv.VideoCapture(stream)
        hasFrame, frame = cap.read()
        inp = cv.dnn.blobFromImage(frame, scalefactor=1.0, size=(500, 500),
                                    mean=(104.00698793, 116.66876762, 122.67891434),
                                    swapRB=False, crop=False)
        self.net.setInput(inp)
        out = self.net.forward()
        out = out[0, 0]
        out = cv.resize(out, (frame.shape[1], frame.shape[0]))
        out = detail_scale * out
        # out = out.astype(np.uint8)
        # out=cv.cvtColor(out,cv.THRESH_BINARY_INV)
        return out

