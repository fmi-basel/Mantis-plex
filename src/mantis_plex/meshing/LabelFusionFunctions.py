# Copyright (C) 2024 Friedrich Miescher Institute for Biomedical Research

##############################################################################
#                                                                            #
# Author: Nicole Repina              <nicole.repina@fmi.ch>                  #
#                                                                            #
##############################################################################


def select_label(seg, label_str):
    # Select label that corresponds to current object, set all other objects to 0
    seg[seg != float(label_str)] = 0
    # Binarize object segmentation image
    seg[seg > 0] = 1

    return seg
