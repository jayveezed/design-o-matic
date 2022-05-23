#!/usr/bin/env python

from gimpfu import *
import os

def auto_verbage(): # CHANGE FUNCTION NAME
    
    verbs_to_gimp = open('C:/PYTHON FINISHED 2022/design-o-matic/verbs_to_gimp.txt', mode='r')
    verified_verbs = verbs_to_gimp.read().splitlines()
    pdb.gimp_context_set_default_colors()
    for verb in verified_verbs:
        
        img = pdb.gimp_file_load('C:/PYTHON FINISHED 2022/design-o-matic/get_stuff_template.xcf', 'get_stuff_template.xcf')
        # gimp.Display(img)
        layer = pdb.gimp_image_set_active_layer(img, img.layers[1]) #SETS ACTIVE CHUFFING LAYER
        pdb.gimp_text_layer_set_text(img.layers[1], "{}!".format(verb).upper()) # APPLY VERB TO TEXT LAYER
        item = pdb.gimp_item_transform_scale(img.layers[1], 135, 2218, 4361, 2920) # SCALE!!!! not sure variable is needed  
        pdb.gimp_image_set_active_layer(img, img.layers[1])
        pdb.gimp_image_select_item(img, 0, item) # selects item (item is a content of a layer in this case)
        pdb.gimp_selection_grow(img, 80) # Grow selection
        pdb.gimp_edit_bucket_fill_full(img.layers[2], 0, 0, 100, 0, FALSE, FALSE, 0, 0, 0) # fill!!!
        pdb.gimp_image_merge_down(img, img.layers[1], 0) # merge down
        item = pdb.gimp_item_transform_rotate(img.layers[1], -0.174533, TRUE, 0, 0) # rotate
        pdb.gimp_image_merge_visible_layers(img, 0) 
        
        new_image = pdb.gimp_image_duplicate(img)
        layer = pdb.gimp_image_merge_visible_layers(new_image, 2)
        
        #### FILE AND FOLDER NAMING ####
        # using .format instead of f-string becaused GIMP FU uses old Python that does not recognise f-strings

        img_folder_name = 'C:/PYTHON FINISHED 2022/design-o-matic/images'
        
        ####
        
        pdb.gimp_file_save(new_image, layer, "{}/get_{}.png".format(img_folder_name, verb).lower(), '?') # '?'  is raw data field
        pdb.gimp_image_delete(new_image) # I think this deletes new_image from memory
        pdb.gimp_image_delete(img)
        
register(
    "python-fu-auto_verbage",
    "AUTO VERBAGE",
    "Applies a chosen verb to a base template image, scales it, adds background, rotates, saves as individual file names",
    "JVZ Designs", "JVZ Designs", "2022",
    "AUTO VERBAGE",
    "", # type of image it works on (*, RGB, RGB*, RGBA, GRAY etc...)
    [
        #(PF_IMAGE, "image", "takes current image", None),
        #(PF_DRAWABLE, "drawable", "Input layer", None)
    ],
    [],
    auto_verbage, menu="<Image>/File")  # second item is menu location

main()
