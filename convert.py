"""
JIS to SJIS2004 conversion utilities
"""

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
    
    if m == 1:
        # JIS X 0208 (first plane) - Standard JIS to Shift JIS conversion
        # Convert ku-ten to JIS code point
        jis_high = k + 0x20  # ku + 0x20
        jis_low = t + 0x20   # ten + 0x20
        
        # Convert JIS to Shift JIS using standard algorithm
        if jis_high % 2 == 1:
            # Odd ku
            s1 = ((jis_high - 0x21) >> 1) + 0x81
            if s1 > 0x9F:
                s1 += 0x40
        else:
            # Even ku  
            s1 = ((jis_high - 0x22) >> 1) + 0x81
            if s1 > 0x9F:
                s1 += 0x40
        
        if jis_high % 2 == 1:
            # Odd ku
            if jis_low < 0x60:
                s2 = jis_low + 0x1F
            else:
                s2 = jis_low + 0x20
        else:
            # Even ku
            s2 = jis_low + 0x7E
            
    else:
        # JIS X 0212 (second plane) - SJIS2004 extension area
        # Map to SJIS2004 extension area (0x8740-0x9FFC, 0xE040-0xFCFC)
        linear_index = (k - 1) * 94 + (t - 1)
        
        if linear_index < 1410:  # First part: 0x8740-0x9FFC
            s1 = 0x87 + (linear_index // 188)
            remainder = linear_index % 188
            if remainder < 63:
                s2 = 0x40 + remainder
            else:
                s2 = 0x41 + remainder
        else:  # Second part: 0xE040-0xFCFC
            adjusted_index = linear_index - 1410
            s1 = 0xE0 + (adjusted_index // 188)
            remainder = adjusted_index % 188
            if remainder < 63:
                s2 = 0x40 + remainder
            else:
                s2 = 0x41 + remainder
    
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
    # Create bytes from the two Shift JIS bytes
    sjis_bytes = bytes([s1, s2])
    
    # Try to decode as Shift JIS (CP932) first
    try:
        unicode_char = sjis_bytes.decode('shift_jis')
        return unicode_char
    except UnicodeDecodeError:
        # If standard Shift JIS fails, try CP932 (Microsoft's extension)
        try:
            unicode_char = sjis_bytes.decode('cp932')
            return unicode_char
        except UnicodeDecodeError:
            # If both fail, try shift_jis2004
            try:
                unicode_char = sjis_bytes.decode('shift_jis-2004')
                return unicode_char
            except (UnicodeDecodeError, LookupError) as e:
                raise UnicodeDecodeError(
                    'shift_jis', 
                    sjis_bytes, 
                    0, 
                    len(sjis_bytes), 
                    f"Cannot decode Shift JIS bytes {s1:02X} {s2:02X}: {str(e)}"
                )


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
