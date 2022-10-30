import argparse
import glob
import cv2
import os
import numpy as np
import pyheif
from PIL import Image

def main():
  '''
  This script converts a batch of images to a different format.
  '''
  cwd = os.getcwd()

  parser = argparse.ArgumentParser()
  parser.add_argument('--input-dir', type=str, default=cwd, help='Directory containing images to convert')
  parser.add_argument('--output-dir', type=str, default=cwd, help='Directory to output converted images')
  parser.add_argument('--input-format', type=str, required=True, help='Format of input images')
  parser.add_argument('--output-format', type=str, default='jpg', help='Format to convert images to')
  parser.add_argument('--max-width', type=int, default=None, help='Maximum width of output images')
  parser.add_argument('--replace', action='store_true', help='Replace input images with converted images')
  args = parser.parse_args()

  input_dir = args.input_dir
  output_dir = args.output_dir
  input_format = args.input_format
  output_format = args.output_format
  replace = args.replace
  
  # collect all images in input directory with input format
  input_images = glob.glob(os.path.join(input_dir, '*.' + input_format))
  print('Found {} images in {} with format {}'.format(len(input_images), input_dir, input_format))

  # convert images
  for input_image in input_images:
    output_image = os.path.join(output_dir, os.path.basename(input_image).replace(input_format, output_format))
    print(f'Converting {input_image} to {output_image}')

    if input_format.lower() == 'heic':
      heif_file = pyheif.read(input_image)
      pil_image = Image.frombytes(
        heif_file.mode, 
        heif_file.size, 
        heif_file.data,
        "raw",
        heif_file.mode,
        heif_file.stride,
      )
      cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    else:
      cv_image = cv2.imread(input_image)

    # resize image if max width is specified
    if args.max_width is not None:
      h, w, _ = cv_image.shape
      if w > args.max_width:
        cv_image = cv2.resize(cv_image, (args.max_width, int(h * args.max_width / w)))
    
    cv2.imwrite(output_image, cv_image)

  # replace input images with converted images
  if replace:
    for input_image in input_images:
      output_image = os.path.join(output_dir, os.path.basename(input_image).replace(input_format, output_format))
      os.remove(input_image)
  
if __name__ == '__main__':
  main()
