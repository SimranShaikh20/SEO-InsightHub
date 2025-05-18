def check_title(title):
    return len(title) > 10 and len(title) < 70

def check_meta_description(meta_desc):
    return len(meta_desc) > 50 and len(meta_desc) < 160

def check_image_alts(images):
    missing_alt = [src for alt, src in images if not alt.strip()]
    return missing_alt  # list of images missing alt text
