import pytesseract
import keras_ocr
import easyocr
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
from os import listdir
import imutils
import sys
from imutils.object_detection import non_max_suppression
from collections import namedtuple
from skimage.io import imread, imshow
from imutils.contours import sort_contours

def ocr_pross():
    template = cv2.imread(r"C:\Users\medez\Desktop\pi\image_ocr\saved_img.jpg")
    image = cv2.imread(r"C:\Users\medez\Desktop\pi\image_ocr\saved_img.jpg")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255,
	cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    def align_images(image, template, maxFeatures=99999999, keepPercent=0.2,debug=False):
        imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        templateGray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        orb = cv2.ORB_create(maxFeatures)
        (kpsA, descsA) = orb.detectAndCompute(imageGray, None)
        (kpsB, descsB) = orb.detectAndCompute(templateGray, None)
        method = cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING
        matcher = cv2.DescriptorMatcher_create(method)
        matches = matcher.match(descsA, descsB, None)
        matches = sorted(matches, key=lambda x:x.distance)
        keep = int(len(matches) * keepPercent)
        matches = matches[:keep]
        if debug:
            matchedVis = cv2.drawMatches(image, kpsA, template, kpsB,matches, None)
            matchedVis = imutils.resize(matchedVis, width=1000)
        ptsA = np.zeros((len(matches), 2), dtype="float")
        ptsB = np.zeros((len(matches), 2), dtype="float")
        for (i, m) in enumerate(matches):
            ptsA[i] = kpsA[m.queryIdx].pt
            ptsB[i] = kpsB[m.trainIdx].pt
        (H, mask) = cv2.findHomography(ptsA, ptsB, method=cv2.RANSAC)
        (h, w) = template.shape[:2]
        aligned = cv2.warpPerspective(image, H, (w, h))
        return aligned
    aligned = align_images(image, template, debug=True)
    aligned = imutils.resize(aligned, width=700)
    template = imutils.resize(template, width=700)
    cv2.imwrite("template.jpg", template)
    stacked = np.hstack([aligned, template])
    overlay = template.copy()
    output = aligned.copy()
    cv2.addWeighted(overlay, 0.5, output, 0.5, 0, output)
    gray = cv2.cvtColor(aligned, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    id_img = aligned[150:200 , 280:480]
    last_name_img = aligned[208:248 , 430:620]
    name_img = aligned[242:320 , 380:625] # [y:y1 , x:x1] zone eli 
    dob = aligned[330:373 , 330:575]
    pob = aligned[374:430 , 370:630]
    text_reader = easyocr.Reader(['ar','en'], gpu = True)
    idn= text_reader.readtext(id_img, detail = 0)
    last_name = text_reader.readtext(last_name_img, detail = 0)
    name = text_reader.readtext(name_img, detail = 0)
    print(idn,last_name,name)  
    return idn, last_name, name


ocr_pross()
