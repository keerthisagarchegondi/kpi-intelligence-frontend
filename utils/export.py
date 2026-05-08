"""
Data Export Utilities

Production-level utilities for exporting data in various formats:
- CSV export with encoding options
- Excel export with multiple sheets and styling
- JSON export
- PDF reports
- Email integration
"""

import pandas as pd
import io
import base64
from datetime import datetime
from typing import Optional, List, Dict, Any, Union
import streamlit as st
import json


class DataExporter:
    """
    Production-level data export handler with multiple format support.
    """
    
    @staticmethod
    def to_csv(
        data: pd.DataFrame,
        filename: Optional[str] = None,
        encoding: str = 'utf-8',
        include_index: bool = False,
        separator: str = ','
    ) -> bytes:
        """
        Export DataFrame to CSV format.
        
        Args:
            data: DataFrame to export
            filename: Optional filename (auto-generated if None)
            encoding: Character encoding
            include_index: Include DataFrame index
            separator: Column separator
        
        Returns:
            CSV data as bytes
        """
        if filename is None:
            filename = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        csv_buffer = io.StringIO()
        data.to_csv(
            csv_buffer,
            index=include_index,
            encoding=encoding,
            sep=separator
        )
        
        return csv_buffer.getvalue().encode(encoding)
    
    @staticmethod
    def to_excel(
        data: Union[pd.DataFrame, Dict[str, pd.DataFrame]],
        filename: Optional[str] = None,
        sheet_name: str = 'Data',
        include_index: bool = False,
        auto_filter: bool = True,
        freeze_panes: Optional[tuple] = (1, 0),
        column_width: int = 15
    ) -> bytes:
        """
        Export data to Excel format with styling.
        
        Args:
            data: Single DataFrame or dict of DataFrames for multiple sheets
            filename: Optional filename
            sheet_name: Sheet name (for single DataFrame)
            include_index: Include DataFrame index
            auto_filter: Add auto-filter to columns
            freeze_panes: Freeze panes position (row, col)
            column_width: Default column width
        
        Returns:
            Excel data as bytes
        """
        if filename is None:
            filename = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            if isinstance(data, dict):
                # Multiple sheets
                for sheet, df in data.items():
                    df.to_excel(
                        writer,
                        sheet_name=sheet,
                        index=include_index
                    )
                    
                    # Apply formatting
                    worksheet = writer.sheets[sheet]
                    
                    if auto_filter:
                        worksheet.auto_filter.ref = worksheet.dimensions
                    
                    if freeze_panes:
                        worksheet.freeze_panes = worksheet.cell(
                            row=freeze_panes[0] + 1,
                            column=freeze_panes[1] + 1
                        )
                    
                    # Set column widths
                    for column in worksheet.columns:
                        worksheet.column_dimensions[column[0].column_letter].width = column_width
            else:
                # Single sheet
                data.to_excel(
                    writer,
                    sheet_name=sheet_name,
                    index=include_index
                )
                
                worksheet = writer.sheets[sheet_name]
                
                if auto_filter:
                    worksheet.auto_filter.ref = worksheet.dimensions
                
                if freeze_panes:
                    worksheet.freeze_panes = worksheet.cell(
                        row=freeze_panes[0] + 1,
                        column=freeze_panes[1] + 1
                    )
                
                # Set column widths
                for column in worksheet.columns:
                    worksheet.column_dimensions[column[0].column_letter].width = column_width
        
        return output.getvalue()
    
    @staticmethod
    def to_json(
        data: pd.DataFrame,
        filename: Optional[str] = None,
        orient: str = 'records',
        indent: int = 2
    ) -> str:
        """
        Export DataFrame to JSON format.
        
        Args:
            data: DataFrame to export
            filename: Optional filename
            orient: JSON orientation ('records', 'index', 'columns', etc.)
            indent: JSON indentation
        
        Returns:
            JSON string
        """
        if filename is None:
            filename = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        return data.to_json(orient=orient, indent=indent, date_format='iso')
    
    @staticmethod
    def create_download_link(
        data: Union[str, bytes],
        filename: str,
        mime_type: str,
        link_text: str = "Download"
    ) -> str:
        """
        Create a download link for data.
        
        Args:
            data: Data to download
            filename: Filename for download
            mime_type: MIME type
            link_text: Text for download link
        
        Returns:
            HTML download link
        """
        if isinstance(data, str):
            data = data.encode()
        
        b64 = base64.b64encode(data).decode()
        href = f'<a href="data:{mime_type};base64,{b64}" download="{filename}">{link_text}</a>'
        return href


class DataValidator:
    """
    Data validation utilities for ensuring data quality.
    """
    
    @staticmethod
    def check_missing_values(data: pd.DataFrame) -> Dict[str, Any]:
        """
        Check for missing values in DataFrame.
        
        Args:
            data: DataFrame to check
        
        Returns:
            Dictionary with missing value statistics
        """
        missing_counts = data.isnull().sum()
        missing_percentages = (missing_counts / len(data) * 100).round(2)
        
        return {
            'total_rows': len(data),
            'total_columns': len(data.columns),
            'columns_with_missing': (missing_counts > 0).sum(),
            'missing_by_column': {
                col: {
                    'count': int(count),
                    'percentage': float(missing_percentages[col])
                }
                for col, count in missing_counts.items()
                if count > 0
            }
        }
    
    @staticmethod
    def check_duplicates(
        data: pd.DataFrame,
        subset: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Check for duplicate rows in DataFrame.
        
        Args:
            data: DataFrame to check
            subset: Columns to consider for duplicate check
        
        Returns:
            Dictionary with duplicate statistics
        """
        duplicates = data.duplicated(subset=subset, keep=False)
        duplicate_count = duplicates.sum()
        
        return {
            'total_rows': len(data),
            'duplicate_rows': int(duplicate_count),
            'duplicate_percentage': float((duplicate_count / len(data) * 100).round(2)),
            'unique_rows': len(data) - int(duplicate_count)
        }
    
    @staticmethod
    def validate_data_types(
        data: pd.DataFrame,
        expected_types: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Validate column data types.
        
        Args:
            data: DataFrame to validate
            expected_types: Expected data types per column
        
        Returns:
            Validation results
        """
        results = {
            'valid': True,
            'mismatches': {}
        }
        
        for col, expected_type in expected_types.items():
            if col not in data.columns:
                results['valid'] = False
                results['mismatches'][col] = {
                    'error': 'Column not found',
                    'expected': expected_type,
                    'actual': None
                }
            elif str(data[col].dtype) != expected_type:
                results['valid'] = False
                results['mismatches'][col] = {
                    'error': 'Type mismatch',
                    'expected': expected_type,
                    'actual': str(data[col].dtype)
                }
        
        return results
    
    @staticmethod
    def get_data_quality_report(data: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate comprehensive data quality report.
        
        Args:
            data: DataFrame to analyze
        
        Returns:
            Comprehensive quality report
        """
        return {
            'shape': {
                'rows': len(data),
                'columns': len(data.columns)
            },
            'missing_values': DataValidator.check_missing_values(data),
            'duplicates': DataValidator.check_duplicates(data),
            'data_types': {
                col: str(dtype)
                for col, dtype in data.dtypes.items()
            },
            'memory_usage': {
                'total_mb': float((data.memory_usage(deep=True).sum() / 1024 / 1024).round(2)),
                'per_column_mb': {
                    col: float((data[col].memory_usage(deep=True) / 1024 / 1024).round(2))
                    for col in data.columns
                }
            },
            'numeric_summary': data.describe().to_dict() if len(data.select_dtypes(include=['number']).columns) > 0 else {}
        }


class ReportGenerator:
    """
    Generate formatted reports with data and visualizations.
    """
    
    @staticmethod
    def generate_summary_report(
        data: pd.DataFrame,
        title: str = "Data Summary Report",
        include_stats: bool = True,
        include_quality: bool = True
    ) -> str:
        """
        Generate a text-based summary report.
        
        Args:
            data: Source data
            title: Report title
            include_stats: Include statistical summary
            include_quality: Include data quality metrics
        
        Returns:
            Formatted report as string
        """
        report = []
        report.append("=" * 80)
        report.append(f"{title}".center(80))
        report.append("=" * 80)
        report.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Basic info
        report.append(f"Total Records: {len(data):,}")
        report.append(f"Total Columns: {len(data.columns)}")
        report.append(f"\nColumn Names: {', '.join(data.columns)}\n")
        
        # Statistics
        if include_stats and len(data.select_dtypes(include=['number']).columns) > 0:
            report.append("\n" + "-" * 80)
            report.append("STATISTICAL SUMMARY")
            report.append("-" * 80)
            report.append(str(data.describe()))
        
        # Quality metrics
        if include_quality:
            report.append("\n" + "-" * 80)
            report.append("DATA QUALITY METRICS")
            report.append("-" * 80)
            
            quality = DataValidator.get_data_quality_report(data)
            
            missing = quality['missing_values']
            report.append(f"\nMissing Values:")
            report.append(f"  - Columns with missing data: {missing['columns_with_missing']}")
            
            duplicates = quality['duplicates']
            report.append(f"\nDuplicate Rows:")
            report.append(f"  - Total duplicates: {duplicates['duplicate_rows']}")
            report.append(f"  - Percentage: {duplicates['duplicate_percentage']}%")
            
            memory = quality['memory_usage']
            report.append(f"\nMemory Usage:")
            report.append(f"  - Total: {memory['total_mb']} MB")
        
        report.append("\n" + "=" * 80)
        
        return "\n".join(report)
    
    @staticmethod
    def export_report_package(
        data: pd.DataFrame,
        report_name: str = "report",
        formats: List[str] = ['csv', 'excel', 'json']
    ) -> Dict[str, bytes]:
        """
        Export data in multiple formats as a package.
        
        Args:
            data: Data to export
            report_name: Base name for files
            formats: List of formats to include
        
        Returns:
            Dictionary mapping format to file content
        """
        exports = {}
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if 'csv' in formats:
            exports['csv'] = DataExporter.to_csv(data)
        
        if 'excel' in formats:
            exports['excel'] = DataExporter.to_excel(data)
        
        if 'json' in formats:
            exports['json'] = DataExporter.to_json(data).encode('utf-8')
        
        if 'summary' in formats:
            summary = ReportGenerator.generate_summary_report(data)
            exports['summary'] = summary.encode('utf-8')
        
        return exports


# Streamlit integration helpers
def render_export_options(
    data: pd.DataFrame,
    key_prefix: str = "export",
    formats: List[str] = ['csv', 'excel', 'json']
):
    """
    Render export options in Streamlit UI.
    
    Args:
        data: Data to export
        key_prefix: Unique key prefix
        formats: Available export formats
    """
    st.markdown("### 💾 Export Options")
    
    export_cols = st.columns(len(formats))
    
    for idx, fmt in enumerate(formats):
        with export_cols[idx]:
            if fmt == 'csv':
                csv_data = DataExporter.to_csv(data)
                st.download_button(
                    label="📄 CSV",
                    data=csv_data,
                    file_name=f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    key=f"{key_prefix}_csv"
                )
            
            elif fmt == 'excel':
                excel_data = DataExporter.to_excel(data)
                st.download_button(
                    label="📊 Excel",
                    data=excel_data,
                    file_name=f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key=f"{key_prefix}_excel"
                )
            
            elif fmt == 'json':
                json_data = DataExporter.to_json(data)
                st.download_button(
                    label="🔗 JSON",
                    data=json_data,
                    file_name=f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    key=f"{key_prefix}_json"
                )


def render_data_quality_dashboard(data: pd.DataFrame):
    """
    Render data quality dashboard in Streamlit.
    
    Args:
        data: Data to analyze
    """
    st.markdown("### 📋 Data Quality Dashboard")
    
    quality_report = DataValidator.get_data_quality_report(data)
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Rows", f"{quality_report['shape']['rows']:,}")
    
    with col2:
        st.metric("Total Columns", quality_report['shape']['columns'])
    
    with col3:
        missing_cols = quality_report['missing_values']['columns_with_missing']
        st.metric("Missing Value Columns", missing_cols)
    
    with col4:
        dup_pct = quality_report['duplicates']['duplicate_percentage']
        st.metric("Duplicate %", f"{dup_pct}%")
    
    # Detailed sections
    with st.expander("📊 Missing Values Details"):
        if quality_report['missing_values']['columns_with_missing'] > 0:
            missing_df = pd.DataFrame([
                {'Column': col, 'Missing Count': info['count'], 'Missing %': info['percentage']}
                for col, info in quality_report['missing_values']['missing_by_column'].items()
            ])
            st.dataframe(missing_df, use_container_width=True)
        else:
            st.success("✅ No missing values found!")
    
    with st.expander("🔍 Duplicate Analysis"):
        dup_info = quality_report['duplicates']
        st.write(f"**Total Duplicates:** {dup_info['duplicate_rows']}")
        st.write(f"**Unique Rows:** {dup_info['unique_rows']}")
        st.write(f"**Duplicate Percentage:** {dup_info['duplicate_percentage']}%")
    
    with st.expander("💾 Memory Usage"):
        memory_info = quality_report['memory_usage']
        st.write(f"**Total Memory:** {memory_info['total_mb']} MB")
        
        memory_df = pd.DataFrame([
            {'Column': col, 'Memory (MB)': mb}
            for col, mb in memory_info['per_column_mb'].items()
        ]).sort_values('Memory (MB)', ascending=False)
        
        st.dataframe(memory_df, use_container_width=True)
