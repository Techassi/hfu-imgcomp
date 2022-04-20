def print_image_list(img_paths: list):
    '''Print a list of images'''
    for i in range(len(img_paths)):
        img_path = img_paths[i]
        print(f"  [{i+1}] {img_path}")
