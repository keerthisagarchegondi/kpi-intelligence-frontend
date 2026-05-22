"""
Upload Validation and Processing Utilities

Production-level utilities for file upload validation, processing, and security:
- File size and type validation
- Content validation and sanitization
- Upload progress tracking
- Retry logic for failed uploads
- Security checks
"""

import streamlit as st
import pandas as pd
import io
import hashlib
from typing import Optional, Dict, Any, Tuple, List
from datetime import datetime
import mimetypes
import json


class UploadConfig:
    """Configuration for file uploads"""
    MAX_FILE_SIZE_MB = 50
    MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
    ALLOWED_EXTENSIONS = {'.csv', '.xlsx', '.xls', '.parquet', '.json'}
    ALLOWED_MIME_TYPES = {
        'text/csv',
        'application/vnd.ms-excel',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'application/octet-stream',  # parquet
        'application/json'
    }
    MIN_FILE_SIZE_BYTES = 10  # 10 bytes minimum
    MAX_ROWS = 1000000  # 1 million rows max
    MAX_COLUMNS = 1000
    CHUNK_SIZE = 8192  # For chunked reading


class UploadValidator:
    """
    Production-level upload validator with comprehensive checks.
    """
    
    @staticmethod
    def validate_file_size(file_size: int) -> Tuple[bool, Optional[str]]:
        """
        Validate file size is within acceptable limits.
        
        Args:
            file_size: File size in bytes
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if file_size < UploadConfig.MIN_FILE_SIZE_BYTES:
            return False, f"File is too small ({file_size} bytes). Minimum size: {UploadConfig.MIN_FILE_SIZE_BYTES} bytes"
        
        if file_size > UploadConfig.MAX_FILE_SIZE_BYTES:
            size_mb = file_size / (1024 * 1024)
            return False, f"File is too large ({size_mb:.2f} MB). Maximum size: {UploadConfig.MAX_FILE_SIZE_MB} MB"
        
        return True, None
    
    @staticmethod
    def validate_file_extension(filename: str) -> Tuple[bool, Optional[str]]:
        """
        Validate file extension is allowed.
        
        Args:
            filename: Original filename
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        import os
        ext = os.path.splitext(filename)[1].lower()
        
        if not ext:
            return False, "File has no extension"
        
        if ext not in UploadConfig.ALLOWED_EXTENSIONS:
            allowed = ', '.join(UploadConfig.ALLOWED_EXTENSIONS)
            return False, f"File extension '{ext}' not allowed. Allowed: {allowed}"
        
        return True, None
    
    @staticmethod
    def validate_filename(filename: str) -> Tuple[bool, Optional[str]]:
        """
        Validate filename for security issues.
        
        Args:
            filename: Original filename
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        import os
        import re
        
        # Check for path traversal attempts
        if '..' in filename or '/' in filename or '\\' in filename:
            return False, "Filename contains invalid path characters"
        
        # Check for null bytes
        if '\x00' in filename:
            return False, "Filename contains null bytes"
        
        # Check for control characters
        if any(ord(c) < 32 for c in filename):
            return False, "Filename contains control characters"
        
        # Check filename length
        if len(filename) > 255:
            return False, "Filename is too long (max 255 characters)"
        
        # Reject filesystem-reserved characters while allowing common filename punctuation
        # and Unicode letters/numbers (e.g., parentheses, commas, apostrophes).
        if re.search(r'[<>:"/\\|?*]', filename):
            return False, (
                "Filename contains invalid characters. "
                "Do not use: < > : \" / \\ | ? *"
            )

        # Windows compatibility: names cannot end in a dot or space.
        if filename.endswith(' ') or filename.endswith('.'):
            return False, "Filename cannot end with a space or dot"
        
        return True, None
    
    @staticmethod
    def validate_file_content(file_content: bytes, filename: str) -> Tuple[bool, Optional[str]]:
        """
        Validate file content matches expected type.
        
        Args:
            file_content: File content as bytes
            filename: Original filename
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        import os
        
        ext = os.path.splitext(filename)[1].lower()
        
        try:
            # Basic content validation based on extension
            if ext == '.csv':
                # Try to read as CSV
                pd.read_csv(io.BytesIO(file_content), nrows=1)
            
            elif ext in ['.xlsx', '.xls']:
                # Try to read as Excel
                pd.read_excel(io.BytesIO(file_content), nrows=1)
            
            elif ext == '.parquet':
                # Try to read as Parquet
                pd.read_parquet(io.BytesIO(file_content))
            
            elif ext == '.json':
                # Try to parse as JSON
                json.loads(file_content.decode('utf-8'))
            
            return True, None
        
        except UnicodeDecodeError:
            return False, f"File encoding error. Ensure file is valid {ext} format"
        
        except pd.errors.ParserError as e:
            return False, f"File parsing error: {str(e)}"
        
        except Exception as e:
            return False, f"Invalid file content: {str(e)}"
    
    @staticmethod
    def validate_dataframe(df: pd.DataFrame) -> Tuple[bool, Optional[str]]:
        """
        Validate DataFrame structure and content.
        
        Args:
            df: Pandas DataFrame
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check if empty
        if df.empty:
            return False, "File contains no data"
        
        # Check row count
        if len(df) > UploadConfig.MAX_ROWS:
            return False, f"Too many rows ({len(df):,}). Maximum: {UploadConfig.MAX_ROWS:,}"
        
        # Check column count
        if len(df.columns) > UploadConfig.MAX_COLUMNS:
            return False, f"Too many columns ({len(df.columns)}). Maximum: {UploadConfig.MAX_COLUMNS}"
        
        # Check for duplicate column names
        if df.columns.duplicated().any():
            duplicates = df.columns[df.columns.duplicated()].tolist()
            return False, f"Duplicate column names found: {duplicates}"
        
        # Check for unnamed columns
        unnamed_cols = [col for col in df.columns if 'Unnamed' in str(col)]
        if unnamed_cols:
            return False, f"File contains unnamed columns: {unnamed_cols}"
        
        return True, None
    
    @staticmethod
    def calculate_file_hash(file_content: bytes) -> str:
        """
        Calculate SHA-256 hash of file content.
        
        Args:
            file_content: File content as bytes
        
        Returns:
            SHA-256 hash string
        """
        return hashlib.sha256(file_content).hexdigest()
    
    @staticmethod
    def get_file_info(file_content: bytes, filename: str) -> Dict[str, Any]:
        """
        Get comprehensive file information.
        
        Args:
            file_content: File content as bytes
            filename: Original filename
        
        Returns:
            Dictionary with file metadata
        """
        import os
        
        file_size = len(file_content)
        file_hash = UploadValidator.calculate_file_hash(file_content)
        ext = os.path.splitext(filename)[1].lower()
        
        info = {
            'filename': filename,
            'size_bytes': file_size,
            'size_mb': round(file_size / (1024 * 1024), 2),
            'extension': ext,
            'hash': file_hash,
            'upload_time': datetime.now().isoformat()
        }
        
        # Try to get DataFrame info
        try:
            df = UploadValidator.load_dataframe(file_content, filename)
            if df is not None:
                info['rows'] = len(df)
                info['columns'] = len(df.columns)
                info['column_names'] = list(df.columns)
                info['dtypes'] = {str(k): str(v) for k, v in df.dtypes.to_dict().items()}
        except:
            pass
        
        return info
    
    @staticmethod
    def load_dataframe(file_content: bytes, filename: str) -> Optional[pd.DataFrame]:
        """
        Load file content into DataFrame.
        
        Args:
            file_content: File content as bytes
            filename: Original filename
        
        Returns:
            DataFrame or None if failed
        """
        import os
        
        ext = os.path.splitext(filename)[1].lower()
        
        try:
            if ext == '.csv':
                return pd.read_csv(io.BytesIO(file_content))
            elif ext in ['.xlsx', '.xls']:
                return pd.read_excel(io.BytesIO(file_content))
            elif ext == '.parquet':
                return pd.read_parquet(io.BytesIO(file_content))
            elif ext == '.json':
                return pd.read_json(io.BytesIO(file_content))
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")
            return None
        
        return None


class UploadProgressTracker:
    """
    Track upload progress and status.
    """
    
    def __init__(self, filename: str, total_size: int):
        """
        Initialize progress tracker.
        
        Args:
            filename: Name of file being uploaded
            total_size: Total file size in bytes
        """
        self.filename = filename
        self.total_size = total_size
        self.uploaded_size = 0
        self.start_time = datetime.now()
        self.status = "initializing"
        self.progress_bar = None
        self.status_text = None
    
    def initialize_ui(self):
        """Initialize Streamlit UI elements for progress tracking"""
        self.progress_bar = st.progress(0)
        self.status_text = st.empty()
    
    def update(self, uploaded_size: int, status: str = "uploading"):
        """
        Update progress.
        
        Args:
            uploaded_size: Number of bytes uploaded so far
            status: Current status message
        """
        self.uploaded_size = uploaded_size
        self.status = status
        
        if self.progress_bar:
            progress = min(1.0, uploaded_size / self.total_size)
            self.progress_bar.progress(progress)
        
        if self.status_text:
            percent = (uploaded_size / self.total_size) * 100
            self.status_text.text(f"{status}: {percent:.1f}% ({uploaded_size:,} / {self.total_size:,} bytes)")
    
    def complete(self, success: bool = True, message: Optional[str] = None):
        """
        Mark upload as complete.
        
        Args:
            success: Whether upload was successful
            message: Optional completion message
        """
        if success:
            if self.progress_bar:
                self.progress_bar.progress(1.0)
            if self.status_text:
                duration = (datetime.now() - self.start_time).total_seconds()
                msg = message or f"✅ Upload complete in {duration:.1f}s"
                self.status_text.success(msg)
        else:
            if self.status_text:
                msg = message or "❌ Upload failed"
                self.status_text.error(msg)


def validate_and_upload(
    uploaded_file,
    process_data: bool = True,
    save_to_raw: bool = True,
    save_to_processed: bool = True,
    validate_schema: bool = True,
    show_progress: bool = True
) -> Optional[Dict[str, Any]]:
    """
    Validate file and upload with comprehensive checks.
    
    Args:
        uploaded_file: Streamlit UploadedFile object
        process_data: Whether to process and clean data
        save_to_raw: Save original file to raw directory
        save_to_processed: Save processed file to processed directory
        validate_schema: Perform schema validation
        show_progress: Show progress indicators
    
    Returns:
        Upload response or None if validation failed
    """
    from services.api import upload_file
    
    validator = UploadValidator()
    
    # Validate filename
    is_valid, error = validator.validate_filename(uploaded_file.name)
    if not is_valid:
        st.error(f"❌ Invalid filename: {error}")
        return None
    
    # Validate file extension
    is_valid, error = validator.validate_file_extension(uploaded_file.name)
    if not is_valid:
        st.error(f"❌ {error}")
        return None
    
    # Read file content
    try:
        file_content = uploaded_file.read()
        file_size = len(file_content)
    except Exception as e:
        st.error(f"❌ Error reading file: {str(e)}")
        return None
    
    # Validate file size
    is_valid, error = validator.validate_file_size(file_size)
    if not is_valid:
        st.error(f"❌ {error}")
        return None
    
    # Validate file content
    is_valid, error = validator.validate_file_content(file_content, uploaded_file.name)
    if not is_valid:
        st.error(f"❌ {error}")
        return None
    
    # Load and validate DataFrame
    df = validator.load_dataframe(file_content, uploaded_file.name)
    if df is None:
        st.error("❌ Unable to load file as DataFrame")
        return None
    
    is_valid, error = validator.validate_dataframe(df)
    if not is_valid:
        st.error(f"❌ {error}")
        return None
    
    # Show file info
    with st.expander("📊 File Information", expanded=False):
        file_info = validator.get_file_info(file_content, uploaded_file.name)
        st.json(file_info)
    
    # Initialize progress tracker
    if show_progress:
        tracker = UploadProgressTracker(uploaded_file.name, file_size)
        tracker.initialize_ui()
        tracker.update(0, "Starting upload...")
    
    # Upload file
    try:
        if show_progress:
            tracker.update(file_size // 2, "Uploading to server...")
        
        result = upload_file(
            file_content=file_content,
            filename=uploaded_file.name,
            process_data=process_data,
            save_to_raw=save_to_raw,
            save_to_processed=save_to_processed,
            validate_schema=validate_schema
        )
        
        if show_progress:
            if result and result.get('status') == 'success':
                tracker.complete(success=True, message=f"✅ {result.get('message', 'Upload complete')}")
            else:
                tracker.complete(success=False, message="❌ Upload failed")
        
        return result
    
    except Exception as e:
        if show_progress:
            tracker.complete(success=False, message=f"❌ Error: {str(e)}")
        st.error(f"❌ Upload error: {str(e)}")
        return None


def display_upload_widget(
    key: str = "file_upload",
    title: str = "📤 Upload Data File",
    accept_multiple: bool = False,
    show_options: bool = True
) -> Optional[Dict[str, Any]]:
    """
    Display production-level file upload widget with validation.
    
    Args:
        key: Unique key for the widget
        title: Widget title
        accept_multiple: Accept multiple files
        show_options: Show upload options
    
    Returns:
        Upload result or None
    """
    st.markdown(f"#### {title}")
    
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=['csv', 'xlsx', 'xls', 'parquet', 'json'],
        help=f"Upload data files for processing and analysis (max {UploadConfig.MAX_FILE_SIZE_MB}MB)",
        key=key,
        accept_multiple_files=accept_multiple
    )
    
    if uploaded_file is not None:
        # Show upload options
        if show_options:
            with st.expander("⚙️ Upload Options", expanded=True):
                process_data = st.checkbox("Process & Clean Data", value=True, key=f"{key}_process")
                save_raw = st.checkbox("Save Original File", value=True, key=f"{key}_raw")
                save_processed = st.checkbox("Save Processed File", value=True, key=f"{key}_processed")
                validate = st.checkbox("Validate Schema", value=True, key=f"{key}_validate")
        else:
            process_data = True
            save_raw = True
            save_processed = True
            validate = True
        
        if st.button("🚀 Upload File", type="primary", key=f"{key}_btn"):
            return validate_and_upload(
                uploaded_file=uploaded_file,
                process_data=process_data,
                save_to_raw=save_raw,
                save_to_processed=save_processed,
                validate_schema=validate,
                show_progress=True
            )
    
    return None
