try:
    import cv2
    import numpy as np
    from PIL import Image
    from skimage.metrics import structural_similarity as ssim
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    print("Warning: OpenCV not available. Image comparison features will be limited.")

import io


def compare_images(master_image_path, product_image_path):
    """
    Compare two images and return similarity score and defect information
    """
    if not CV2_AVAILABLE:
        return {
            'similarity_score': 0,
            'defects': [],
            'defect_count': 0,
            'error': 'OpenCV not installed. Please install: pip install opencv-python numpy scikit-image'
        }
    
    # Load images
    master = cv2.imread(master_image_path)
    product = cv2.imread(product_image_path)
    
    if master is None or product is None:
        return None, "Error loading images"
    
    # Resize product image to match master
    product = cv2.resize(product, (master.shape[1], master.shape[0]))
    
    # Convert to grayscale
    master_gray = cv2.cvtColor(master, cv2.COLOR_BGR2GRAY)
    product_gray = cv2.cvtColor(product, cv2.COLOR_BGR2GRAY)
    
    # Calculate SSIM
    similarity_score, diff = ssim(master_gray, product_gray, full=True)
    similarity_percentage = similarity_score * 100
    
    # Convert difference to uint8
    diff = (diff * 255).astype("uint8")
    
    # Threshold the difference image
    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    defects = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 100:  # Filter small differences
            x, y, w, h = cv2.boundingRect(contour)
            defects.append({
                'x': int(x),
                'y': int(y),
                'width': int(w),
                'height': int(h),
                'area': int(area)
            })
    
    return {
        'similarity_score': round(similarity_percentage, 2),
        'defects': defects,
        'defect_count': len(defects)
    }


def analyze_defects(defects, similarity_score):
    """
    Analyze defects and provide fix instructions
    """
    if similarity_score >= 95:
        return "Product matches master sample. No defects detected.", ""
    
    defect_description = []
    fix_instructions = []
    
    if similarity_score < 70:
        defect_description.append("Major differences detected from master sample")
        fix_instructions.append("1. Check if correct mould is being used")
        fix_instructions.append("2. Verify material type and color match specifications")
        fix_instructions.append("3. Review machine settings (temperature, pressure, cycle time)")
    elif similarity_score < 85:
        defect_description.append("Moderate differences detected")
        fix_instructions.append("1. Check injection pressure and holding pressure")
        fix_instructions.append("2. Verify cooling time is adequate")
        fix_instructions.append("3. Inspect mould for wear or damage")
    else:
        defect_description.append("Minor differences detected")
        fix_instructions.append("1. Fine-tune injection speed")
        fix_instructions.append("2. Check material temperature")
        fix_instructions.append("3. Verify mould temperature is consistent")
    
    if len(defects) > 0:
        defect_description.append(f"{len(defects)} defect area(s) identified")
        
        # Analyze defect patterns
        large_defects = [d for d in defects if d['area'] > 1000]
        if large_defects:
            fix_instructions.append("4. Large defects detected - check for:")
            fix_instructions.append("   - Short shots (incomplete filling)")
            fix_instructions.append("   - Flash (excess material)")
            fix_instructions.append("   - Sink marks")
        
        small_defects = [d for d in defects if d['area'] <= 1000]
        if small_defects:
            fix_instructions.append("5. Small defects detected - check for:")
            fix_instructions.append("   - Surface blemishes")
            fix_instructions.append("   - Flow marks")
            fix_instructions.append("   - Contamination")
    
    return "\n".join(defect_description), "\n".join(fix_instructions)


def get_defect_fix_instructions(defect_type):
    """
    Get specific fix instructions based on defect type
    """
    defect_fixes = {
        'short_shot': {
            'causes': 'Insufficient material, low injection pressure, cold material',
            'fixes': [
                'Increase injection pressure',
                'Increase material temperature',
                'Increase injection speed',
                'Check for material blockage',
                'Verify adequate material supply'
            ]
        },
        'flash': {
            'causes': 'Excessive injection pressure, worn mould, insufficient clamping',
            'fixes': [
                'Reduce injection pressure',
                'Reduce material temperature',
                'Increase clamping force',
                'Inspect and repair mould parting line',
                'Check mould alignment'
            ]
        },
        'sink_marks': {
            'causes': 'Insufficient packing pressure, inadequate cooling',
            'fixes': [
                'Increase packing pressure',
                'Extend packing time',
                'Reduce material temperature',
                'Increase cooling time',
                'Optimize gate location'
            ]
        },
        'warpage': {
            'causes': 'Uneven cooling, high material temperature, residual stress',
            'fixes': [
                'Optimize cooling system',
                'Reduce material temperature',
                'Adjust packing pressure',
                'Increase cooling time',
                'Check mould temperature uniformity'
            ]
        },
        'flow_marks': {
            'causes': 'Low injection speed, cold material, poor venting',
            'fixes': [
                'Increase injection speed',
                'Increase material temperature',
                'Improve mould venting',
                'Optimize gate location',
                'Increase mould temperature'
            ]
        }
    }
    
    return defect_fixes.get(defect_type, {})
