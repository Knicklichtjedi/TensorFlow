## filters folder

**This folder contains the code for pre-image-filtering using digital image processing.**

- image_filter.py: controls the processes needed for the preparation of the incoming images
    - image_filter folder: contains all methods for image processing
    
        binary_filter.py              - all methods that make rgb to black and white
        
        center_of_mass_and_fillout.py - the com method and the fillout method
        
        contours.py                   - all methods that work with rectangles & cv2.contours
        
        cropping_scaling_borders.py   - all cropping and scaling methods and adding / deleting borders
        
        rotation.py                   - methods to rotate an image / get rotation from images
        
- collect_data.py: gets multiple images from an image file and saves them in a directory with the correct label.
- prepare_data.py: reads images and converts them into the correct shape for a CNN datset.
