"""
JIS to SJIS2004 conversion utilities
"""

def calculate_s1(m, k):
    """Calculate S1 byte for SJIS conversion"""
    if m == 1:
        if 1 <= k <= 62:
            return (k + 0x101) // 2
        elif 63 <= k <= 94:
            return (k + 0x181) // 2
    elif m == 2:
        if k in {1, 3, 4, 5, 8, 12, 13, 14, 15}:
            return (k + 0x1DF) // 2 - (k // 8) * 3
        elif 78 <= k <= 94:
            return (k + 0x19B) // 2
    return None


def calculate_s2(k, t):
    """Calculate S2 byte for SJIS conversion"""
    if k % 2 == 1:  # k が奇数の場合
        if 1 <= t <= 63:
            return t + 0x3F
        elif 64 <= t <= 94:
            return t + 0x40
    else:  # k が偶数の場合
        return t + 0x9E
    return None


def jis_to_sjis(m, k, t):
    """
    Convert JIS area-ku-ten coordinates to Shift JIS bytes
    
    Args:
        m (int): Area number (1st digit)
        k (int): Ku number (2nd-3rd digits)
        t (int): Ten number (4th-5th digits)
    
    Returns:
        tuple: (s1, s2) Shift JIS first and second bytes
    
    Raises:
        ValueError: If coordinates are out of valid range
    """
    # Validate input ranges
    if not (1 <= m <= 2):
        raise ValueError(f"Invalid area number: {m}. Must be 1 or 2.")
    
    if not (1 <= k <= 94):
        raise ValueError(f"Invalid ku number: {k}. Must be between 1 and 94.")
    
    if not (1 <= t <= 94):
        raise ValueError(f"Invalid ten number: {t}. Must be between 1 and 94.")
    
    s1 = calculate_s1(m, k)
    s2 = calculate_s2(k, t)

    if s1 is None or s2 is None:
        raise ValueError("Invalid input for JIS to Shift JIS conversion.")

    return s1, s2


def sjis_to_unicode(s1, s2):
    """
    Convert Shift JIS bytes to Unicode character
    
    Args:
        s1 (int): First Shift JIS byte
        s2 (int): Second Shift JIS byte
    
    Returns:
        str: Unicode character
    
    Raises:
        UnicodeDecodeError: If bytes cannot be decoded
    """
    sjis_bytes = bytearray([s1, s2])
    return sjis_bytes.decode("sjis_2004")


def convert_jis_code(jis_input):
    """
    Convert a 5-digit JIS area-ku-ten code to Unicode character
    
    Args:
        jis_input (str): 5-digit JIS code string
    
    Returns:
        tuple: (success, result_or_error, debug_info)
    """
    debug_info = None
    
    try:
        # Validate input format
        if not jis_input.isdigit() or len(jis_input) != 5:
            return False, "Input must be exactly 5 digits", None
        
        # Parse area, ku, ten
        m = int(jis_input[0])        # Area (1st digit)
        k = int(jis_input[1:3])      # Ku (2nd-3rd digits)  
        t = int(jis_input[3:5])      # Ten (4th-5th digits)
        
        debug_info = {
            'area': m,
            'ku': k,
            'ten': t,
            'sjis_bytes': None,
            'sjis_hex': ""
        }
        
        # Convert JIS to SJIS
        s1, s2 = jis_to_sjis(m, k, t)
        debug_info['sjis_bytes'] = f"({s1}, {s2})"
        debug_info['sjis_hex'] = f"{s1:02X} {s2:02X}"
        
        # Convert SJIS to Unicode
        unicode_char = sjis_to_unicode(s1, s2)
        
        return True, unicode_char, debug_info
        
    except UnicodeDecodeError as e:
        return False, f"Character encoding error: {str(e)}", debug_info
    except ValueError as e:
        return False, f"Conversion error: {str(e)}", debug_info
    except Exception as e:
        return False, f"Unexpected error: {str(e)}", debug_info
