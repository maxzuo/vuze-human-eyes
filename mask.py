import os
import shutil
import argparse

import numpy as np
import cv2
import pyexiv2 as pex

def mask(left_image_path:str, right_image_path:str, blur:int=0, blur_strength:float=5.):
    left_image = cv2.imread(left_image_path)
    right_image = cv2.imread(right_image_path)

    left_mask = np.load("mask.npy").astype(np.uint8) * 255
    if blur > 0:
        left_mask = cv2.dilate(left_mask, (blur, blur))
        left_mask = cv2.GaussianBlur(left_mask, (blur, blur), blur_strength, borderType=cv2.BORDER_CONSTANT)
    right_mask = np.fliplr(left_mask)

    right_mask = cv2.resize(right_mask, right_image.shape[:2], interpolation=cv2.INTER_NEAREST)
    left_mask = cv2.resize(left_mask, left_image.shape[:2], interpolation=cv2.INTER_NEAREST)

    left_image = left_image * (cv2.cvtColor(left_mask, cv2.COLOR_GRAY2BGR) / 255)
    right_image = right_image * (cv2.cvtColor(right_mask, cv2.COLOR_GRAY2BGR) / 255)

    left_image_path_new = os.path.join(os.path.dirname(left_image_path), "masked_"+os.path.basename(left_image_path))
    right_image_path_new = os.path.join(os.path.dirname(right_image_path), "masked_"+os.path.basename(right_image_path))

    cv2.imwrite(left_image_path_new[:-3]+"jpg", left_image.astype(np.uint8))
    shutil.move(left_image_path_new[:-3]+"jpg", left_image_path_new)
    cv2.imwrite(right_image_path_new, right_image.astype(np.uint8))


    with pex.Image(left_image_path) as l_img:
        l_meta = l_img.read_xmp()
    with pex.Image(left_image_path_new) as l_img_new:
        l_img_new.modify_xmp(l_meta)

    with pex.Image(right_image_path) as r_img:
        r_meta = r_img.read_xmp()
    with pex.Image(right_image_path_new) as r_img_new:
        r_img_new.modify_xmp(r_meta)



if __name__ == "__main__":
    parser = argparse.ArgumentParser("A script to produce accurate masked FOV of cmaeras")

    parser.add_argument("--eye", '-e', help="path to image of any eye (left or right)", type=str, required=True)
    parser.add_argument("--blur_edges", '-b', help='set to something positive, odd integer to blur the edges', type=int, required=False, default=0)
    parser.add_argument("--blur_strength", '-s', help="how strong to blur it", type=float, default=5.)

    args = parser.parse_args()

    assert args.eye.lower().endswith('.jp2') or args.eye.lower().endswith('.jpg'), "The filepath you gave is not a valid VUZE image (.jp2, jpg): " + args.eye
    assert os.path.isfile(args.eye), "Eye filepath does not exist: " + args.eye

    eye_path = args.eye.rsplit('.',maxsplit=1)[0]

    left = eye_path+".jp2"
    right = eye_path+".jpg"

    mask(left, right, blur=args.blur_edges, blur_strength=args.blur_strength)