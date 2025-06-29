# JIS to SJIS2004 Character Converter

## Overview

This is a Streamlit web application that converts JIS (Japanese Industrial Standards) area-ku-ten codes to SJIS2004 characters. The application takes 5-digit JIS codes as input and displays the corresponding Japanese characters in real-time. It's designed for users who need to convert between different Japanese character encoding systems.

## System Architecture

The application follows a simple two-tier architecture:

1. **Frontend**: Streamlit-based web interface for user interaction
2. **Backend**: Python conversion logic handling JIS to SJIS2004 transformation

The architecture prioritizes simplicity and ease of use, with real-time conversion capabilities and a clean, centered layout design.

## Key Components

### Frontend (app.py)
- **Streamlit Web Interface**: Provides a user-friendly web UI with centered layout
- **Real-time Input Processing**: Automatically converts input when exactly 5 digits are entered
- **Character Display**: Shows converted characters in large, readable format
- **Copy Functionality**: Allows users to copy converted characters to clipboard
- **Input Validation**: Restricts input to exactly 5 digits with placeholder guidance

### Backend (convert.py)
- **JIS to SJIS Conversion Engine**: Core conversion logic handling coordinate transformation
- **Input Validation**: Validates area numbers (1-2), ku numbers (1-94), and ten numbers (1-94)
- **Multi-plane Support**: Handles both JIS X 0208 (first plane) and JIS X 0212 (second plane) character sets
- **Error Handling**: Provides detailed error messages for invalid input ranges

## Data Flow

1. User enters 5-digit JIS code in the web interface
2. Input is automatically validated for length (exactly 5 digits)
3. Code is parsed into area (1 digit), ku (2 digits), and ten (2 digits) components
4. Conversion function validates each component's range
5. JIS coordinates are converted to JIS code points
6. JIS codes are transformed to Shift JIS bytes
7. Final character is displayed in the web interface with copy functionality

## External Dependencies

- **Streamlit**: Web application framework for creating the user interface
- **pyperclip**: Cross-platform clipboard functionality for copy operations
- **Python Standard Library**: Core Python functionality for mathematical operations and string handling

The application uses minimal external dependencies to maintain simplicity and reduce potential compatibility issues.

## Deployment Strategy

The application is designed for deployment on Replit or similar Python hosting platforms. Key deployment considerations:

- **Single-file Configuration**: Streamlit app can be run directly with `streamlit run app.py`
- **No Database Required**: All conversion logic is computational, requiring no persistent storage
- **Lightweight Dependencies**: Only requires Streamlit and pyperclip, both installable via pip
- **Cross-platform Compatibility**: Pure Python implementation works across different operating systems

## Changelog

```
Changelog:
- June 29, 2025. Initial setup
```

## User Preferences

```
Preferred communication style: Simple, everyday language.
```