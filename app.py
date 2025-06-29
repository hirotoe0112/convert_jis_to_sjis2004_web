"""
Streamlit Web Application for JIS to SJIS2004 Character Conversion
"""

import streamlit as st
import pyperclip
from convert import convert_jis_code

def main():
    """Main Streamlit application"""
    
    # Page configuration
    st.set_page_config(
        page_title="JIS to SJIS2004 Converter",
        page_icon="🔤",
        layout="centered"
    )
    
    # Application title
    st.title("🔤 JIS to SJIS2004 Character Converter")
    st.markdown("Convert JIS area-ku-ten codes (5 digits) to SJIS2004 characters")
    
    # Input section
    st.subheader("Input")
    jis_input = st.text_input(
        "Enter 5-digit JIS area-ku-ten code:",
        placeholder="12345",
        max_chars=5,
        key="jis_input"
    )
    
    # Real-time conversion when input is exactly 5 digits
    if jis_input and len(jis_input) == 5:
        success, result, debug_info = convert_jis_code(jis_input)
        
        if success:
            # Display result section
            st.subheader("Result")
            
            # Large character display
            st.markdown(
                f"<div style='text-align: center; font-size: 80px; margin: 20px 0;'>{result}</div>",
                unsafe_allow_html=True
            )
            
            # Copy functionality using Streamlit's built-in clipboard
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                # Use st.code with copy button functionality
                st.code(result, language=None)
                st.caption("👆 Click the copy icon in the code box above to copy the character")
            
            # Debug information (expandable)
            if debug_info:
                with st.expander("🔍 Conversion Details"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**JIS Coordinates:**")
                        st.write(f"• Area: {debug_info['area']}")
                        st.write(f"• Ku: {debug_info['ku']:02d}")
                        st.write(f"• Ten: {debug_info['ten']:02d}")
                    
                    with col2:
                        st.write("**Shift JIS:**")
                        st.write(f"• Bytes: {debug_info['sjis_hex']}")
                        st.write(f"• Decimal: {debug_info['sjis_bytes']}")
        
        else:
            # Display error
            st.subheader("Error")
            st.error(result)
            
            if debug_info:
                with st.expander("🔍 Debug Information"):
                    st.json(debug_info)
    
    elif jis_input and len(jis_input) < 5:
        st.info(f"Enter {5 - len(jis_input)} more digit(s) to convert")
    elif jis_input and len(jis_input) > 5:
        st.warning("Input must be exactly 5 digits")
    
    # Help section
    st.markdown("---")
    with st.expander("ℹ️ How to Use"):
        st.markdown("""
        **JIS Area-Ku-Ten Code Format:**
        - **5 digits total**: AKKTT
        - **A**: Area number (1 or 2)
        - **KK**: Ku number (01-94) 
        - **TT**: Ten number (01-94)
        
        **Examples:**
        - `10101` → Area 1, Ku 01, Ten 01
        - `20194` → Area 2, Ku 01, Ten 94
        
        **Supported Character Sets:**
        - Area 1: JIS X 0208 (standard Japanese characters)
        - Area 2: JIS X 0212 (supplementary characters)
        """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666; font-size: 0.8em;'>"
        "JIS to SJIS2004 Character Converter | Built with Streamlit"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
