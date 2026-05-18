# 📊 KPI Intelligence & Reporting Platform

A production-level business intelligence frontend application built with Streamlit, featuring comprehensive KPI data analysis, advanced reporting capabilities, and interactive data visualizations.

## 🌟 Key Features

### 🎯 **Production-Level Implementation**
- ✅ Comprehensive KPI data fetching via API with fallback
- ✅ Advanced interactive report tables with filtering, sorting, pagination
- ✅ **Production-level loading states** - Spinners, progress bars, skeleton loaders
- ✅ **Comprehensive error handling** - User-friendly error messages with recovery suggestions
- ✅ Multi-format data export (CSV, Excel, JSON)
- ✅ Real-time data visualization
- ✅ Data quality assessment tools
- ✅ Responsive design with intuitive UI
- ✅ **Graceful degradation** - Automatic fallback to sample data
- ✅ **Retry mechanisms** - Smart retry for transient errors

### 📈 **Multiple Report Types**
- **Sales Overview** - Comprehensive sales data with trends
- **Product Performance** - Product-level analytics and metrics
- **Customer Analytics** - Customer behavior and segmentation
- **Revenue Breakdown** - Revenue analysis by dimensions
- **Top Performers** - Rankings by various metrics
- **KPI Summary** - Aggregated business metrics

### 🔧 **Advanced Features**
- **Global Search** - Search across all columns
- **Advanced Filters** - Column-specific filtering
- **Pagination** - Handle large datasets efficiently
- **Column Selection** - Show/hide columns dynamically
- **Export** - Download data in multiple formats
- **Conditional Formatting** - Visual data highlighting
- **Summary Statistics** - Automatic metric calculations
- **Loading Indicators** - Visual feedback for all operations
- **Error Recovery** - Actionable error messages with suggestions

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd kpi-intelligence-frontend
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app/main.py
   ```

4. **Access the application**
   - Open your browser to `http://localhost:8501`
   - Navigate through different pages using the sidebar

## 📁 Project Structure

```
kpi-intelligence-frontend/
├── app/
│   ├── main.py                 # Main application entry point
│   └── pages/                  # Application pages
│       ├── charts_demo.py      # Chart demonstrations
│       ├── dashboard.py        # Main dashboard
│       ├── filter_demo.py      # Filter demonstrations
│       ├── reports.py          # 🆕 Reports & data tables
│       ├── retention.py        # Retention metrics
│       └── revenue.py          # Revenue analytics
├── components/                 # Reusable UI components
│   ├── alerts.py              # Alert components
│   ├── charts.py              # Chart components
│   ├── filters.py             # Filter components
│   └── tables.py              # 🆕 Table components
├── services/                  # Backend services
│   └── api.py                 # 🔄 Enhanced API service
├── utils/                     # 🆕 Utility modules
│   ├── __init__.py
│   ├── export.py             # Data export utilities
│   └── data_processing.py    # Data processing utilities
├── assets/                    # Static assets
│   └── styles.css            # Custom CSS styles
├── requirements.txt           # 🔄 Python dependencies
├── README.md                  # This file
└── FEATURES.md               # 🆕 Detailed features documentation
```

## 📖 Usage Guide

### Accessing Reports

1. Launch the application
2. Navigate to **Reports** from the sidebar
3. Select a report type from the dropdown
4. Apply filters as needed
5. Interact with the data table
6. Export data in your preferred format

### Using the Interactive Table

- **Search**: Use the search box to filter data globally
- **Sort**: Click column headers to sort data
- **Filter**: Apply column-specific filters via "Advanced Filters"
- **Columns**: Select which columns to display via "Columns" menu
- **Export**: Download data via "Export" menu
- **Paginate**: Navigate through pages using pagination controls

### API Integration

The application connects to a backend API for real-time data. If the backend is unavailable, it automatically falls back to sample data for demonstration purposes.

**Configure backend URL** in `services/api.py`:
```python
class APIConfig:
    BASE_URL = "http://localhost:8000"  # Change to your backend URL
```

## 🔧 Configuration

### API Settings
Edit `services/api.py` to configure:
- Backend URL
- Timeout settings
- Retry logic
- Cache duration

### Table Settings
Edit `components/tables.py` to configure:
- Default page size
- Available page sizes
- Maximum export rows

## 📊 Features Documentation

For detailed documentation of all features, see [FEATURES.md](FEATURES.md).

Key documentation sections:
- API Enhancement Details
- Table Component Features
- Export Utilities
- Data Processing Tools
- Usage Examples
- Testing Guide

## 🛠️ Technology Stack

- **Frontend Framework**: Streamlit 1.32.0
- **Data Processing**: Pandas 2.2.1
- **Visualizations**: Plotly 5.20.0
- **API Communication**: Requests 2.31.0
- **Numerical Computing**: NumPy 1.26.4
- **Excel Export**: OpenPyXL 3.1.2

## 📦 Dependencies

All required packages are listed in `requirements.txt`:

```
streamlit==1.32.0
pandas==2.2.1
plotly==5.20.0
requests==2.31.0
numpy==1.26.4
openpyxl==3.1.2
```

Install all at once:
```bash
pip install -r requirements.txt
```

## 🎨 Key Components

### 1. Enhanced API Service (`services/api.py`)
- Comprehensive KPI data fetching
- Automatic retry with exponential backoff
- Response caching
- Graceful fallback to sample data

### 2. Interactive Tables (`components/tables.py`)
- Search and filter capabilities
- Pagination for large datasets
- Column selection
- Multi-format export
- Conditional formatting

### 3. Reports Page (`app/pages/reports.py`)
- Multiple report types
- Interactive visualizations
- Summary metrics
- Advanced filtering
- Data export

### 4. Loading States (`components/loading.py`)
- Spinner indicators
- Progress bars
- Skeleton loaders
- Multi-stage progress
- Loading timers
- Batch processing indicators

### 5. Error Handling (`components/errors.py`)
- Error categorization (Network, API, Validation, etc.)
- Severity levels (Info, Warning, Error, Critical)
- User-friendly messages
- Recovery suggestions
- Retry mechanisms
- Error logging

### 6. Export Utilities (`utils/export.py`)
- CSV, Excel, JSON export
- Data validation
- Quality reporting
- Streamlit integration

### 7. Data Processing (`utils/data_processing.py`)
- Data cleaning
- Transformation utilities
- KPI calculations
- Aggregation tools

## 🧪 Testing

### Manual Testing
1. Start the application
2. Navigate to each page
3. Test all interactive features
4. Verify data exports
5. Check error handling

### Validation Checklist
- ✅ All pages load without errors
- ✅ API calls work or fallback gracefully
- ✅ Tables display and paginate correctly
- ✅ Filters apply as expected
- ✅ Exports generate valid files
- ✅ Visualizations render properly

## 🎯 Production Features

### Performance
- Efficient caching mechanism
- Pagination for large datasets
- Optimized data structures
- Lazy loading

### Security
- Input validation
- Error handling
- Timeout management
- Safe data serialization

### User Experience
- Loading indicators
- Clear error messages
- Intuitive navigation
- Responsive design
- Fallback mechanisms

### Maintainability
- Modular architecture
- Clear documentation
- Type hints
- Consistent naming
- Reusable components

## 🔄 Backend Integration

This frontend is designed to work with a REST API backend. Expected API endpoints:

- `GET /api/v1/kpi/overview` - KPI overview data
- `GET /api/v1/reports/list` - Available reports
- `GET /api/v1/reports/{report_id}` - Report data
- `GET /api/v1/kpi/timeseries` - Time series data
- `GET /api/v1/kpi/compare` - Period comparison
- `GET /api/v1/kpi/top-performers` - Top performers

If backend is unavailable, the application uses realistic sample data.

## 📈 Future Enhancements

Potential improvements:
- Real-time data streaming
- Advanced analytics (ML/AI)
- Custom dashboard builder
- Scheduled reports
- Email integration
- Multi-user authentication
- Mobile app
- Dark mode

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

[Add your license information here]

## 📞 Support

For questions or issues:
1. Check [FEATURES.md](FEATURES.md) for detailed documentation
2. Review inline code comments
3. Check error messages in the UI

## ✨ New in This Release

### Version 2.1 (May 2026) - Latest
- ✅ **Loading States** - Production-level loading indicators
- ✅ **Error Handling** - Comprehensive error management system
- ✅ **User Feedback** - Clear loading and error messages
- ✅ **Retry Mechanisms** - Automatic retry for transient errors
- ✅ **Error Recovery** - Actionable suggestions for users
- ✅ **Status Tracking** - API call status monitoring

### Version 2.0 (May 2026)
- ✅ **Enhanced API Service** - Comprehensive KPI endpoints
- ✅ **Interactive Tables** - Advanced filtering and export
- ✅ **Reports Page** - Multiple report types
- ✅ **Export Utilities** - Multi-format data export
- ✅ **Data Processing** - Complete transformation suite
- ✅ **Production Ready** - Enterprise-level code quality

---

**Built with ❤️ using Streamlit**

*Last Updated: May 11, 2026*# 📊 KPI Intelligence & Reporting Platform

A production-level business intelligence frontend application built with Streamlit, featuring comprehensive KPI data analysis, advanced reporting capabilities, and interactive data visualizations.

## 🌟 Key Features

### 🎯 **Production-Level Implementation**
- ✅ Comprehensive KPI data fetching via API with fallback
- ✅ Advanced interactive report tables with filtering, sorting, pagination
- ✅ **Production-level loading states** - Spinners, progress bars, skeleton loaders
- ✅ **Comprehensive error handling** - User-friendly error messages with recovery suggestions
- ✅ Multi-format data export (CSV, Excel, JSON)
- ✅ Real-time data visualization
- ✅ Data quality assessment tools
- ✅ Responsive design with intuitive UI
- ✅ **Graceful degradation** - Automatic fallback to sample data
- ✅ **Retry mechanisms** - Smart retry for transient errors

### 📈 **Multiple Report Types**
- **Sales Overview** - Comprehensive sales data with trends
- **Product Performance** - Product-level analytics and metrics
- **Customer Analytics** - Customer behavior and segmentation
- **Revenue Breakdown** - Revenue analysis by dimensions
- **Top Performers** - Rankings by various metrics
- **KPI Summary** - Aggregated business metrics

### 🔧 **Advanced Features**
- **Global Search** - Search across all columns
- **Advanced Filters** - Column-specific filtering
- **Pagination** - Handle large datasets efficiently
- **Column Selection** - Show/hide columns dynamically
- **Export** - Download data in multiple formats
- **Conditional Formatting** - Visual data highlighting
- **Summary Statistics** - Automatic metric calculations
- **Loading Indicators** - Visual feedback for all operations
- **Error Recovery** - Actionable error messages with suggestions

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd kpi-intelligence-frontend
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app/main.py
   ```

4. **Access the application**
   - Open your browser to `http://localhost:8501`
   - Navigate through different pages using the sidebar

## 📁 Project Structure

```
kpi-intelligence-frontend/
├── app/
│   ├── main.py                 # Main application entry point
│   └── pages/                  # Application pages
│       ├── charts_demo.py      # Chart demonstrations
│       ├── dashboard.py        # Main dashboard
│       ├── filter_demo.py      # Filter demonstrations
│       ├── reports.py          # 🆕 Reports & data tables
│       ├── retention.py        # Retention metrics
│       └── revenue.py          # Revenue analytics
├── components/                 # Reusable UI components
│   ├── alerts.py              # Alert components
│   ├── charts.py              # Chart components
│   ├── filters.py             # Filter components
│   └── tables.py              # 🆕 Table components
├── services/                  # Backend services
│   └── api.py                 # 🔄 Enhanced API service
├── utils/                     # 🆕 Utility modules
│   ├── __init__.py
│   ├── export.py             # Data export utilities
│   └── data_processing.py    # Data processing utilities
├── assets/                    # Static assets
│   └── styles.css            # Custom CSS styles
├── requirements.txt           # 🔄 Python dependencies
├── README.md                  # This file
└── FEATURES.md               # 🆕 Detailed features documentation
```

## 📖 Usage Guide

### Accessing Reports

1. Launch the application
2. Navigate to **Reports** from the sidebar
3. Select a report type from the dropdown
4. Apply filters as needed
5. Interact with the data table
6. Export data in your preferred format

### Using the Interactive Table

- **Search**: Use the search box to filter data globally
- **Sort**: Click column headers to sort data
- **Filter**: Apply column-specific filters via "Advanced Filters"
- **Columns**: Select which columns to display via "Columns" menu
- **Export**: Download data via "Export" menu
- **Paginate**: Navigate through pages using pagination controls

### API Integration

The application connects to a backend API for real-time data. If the backend is unavailable, it automatically falls back to sample data for demonstration purposes.

**Configure backend URL** in `services/api.py`:
```python
class APIConfig:
    BASE_URL = "http://localhost:8000"  # Change to your backend URL
```

## 🔧 Configuration

### API Settings
Edit `services/api.py` to configure:
- Backend URL
- Timeout settings
- Retry logic
- Cache duration

### Table Settings
Edit `components/tables.py` to configure:
- Default page size
- Available page sizes
- Maximum export rows

## 📊 Features Documentation

For detailed documentation of all features, see [FEATURES.md](FEATURES.md).

Key documentation sections:
- API Enhancement Details
- Table Component Features
- Export Utilities
- Data Processing Tools
- Usage Examples
- Testing Guide

## 🛠️ Technology Stack

- **Frontend Framework**: Streamlit 1.32.0
- **Data Processing**: Pandas 2.2.1
- **Visualizations**: Plotly 5.20.0
- **API Communication**: Requests 2.31.0
- **Numerical Computing**: NumPy 1.26.4
- **Excel Export**: OpenPyXL 3.1.2

## 📦 Dependencies

All required packages are listed in `requirements.txt`:

```
streamlit==1.32.0
pandas==2.2.1
plotly==5.20.0
requests==2.31.0
numpy==1.26.4
openpyxl==3.1.2
```

Install all at once:
```bash
pip install -r requirements.txt
```

## 🎨 Key Components

### 1. Enhanced API Service (`services/api.py`)
- Comprehensive KPI data fetching
- Automatic retry with exponential backoff
- Response caching
- Graceful fallback to sample data

### 2. Interactive Tables (`components/tables.py`)
- Search and filter capabilities
- Pagination for large datasets
- Column selection
- Multi-format export
- Conditional formatting

### 3. Reports Page (`app/pages/reports.py`)
- Multiple report types
- Interactive visualizations
- Summary metrics
- Advanced filtering
- Data export

### 4. Loading States (`components/loading.py`)
- Spinner indicators
- Progress bars
- Skeleton loaders
- Multi-stage progress
- Loading timers
- Batch processing indicators

### 5. Error Handling (`components/errors.py`)
- Error categorization (Network, API, Validation, etc.)
- Severity levels (Info, Warning, Error, Critical)
- User-friendly messages
- Recovery suggestions
- Retry mechanisms
- Error logging

### 6. Export Utilities (`utils/export.py`)
- CSV, Excel, JSON export
- Data validation
- Quality reporting
- Streamlit integration

### 7. Data Processing (`utils/data_processing.py`)
- Data cleaning
- Transformation utilities
- KPI calculations
- Aggregation tools

## 🧪 Testing

### Manual Testing
1. Start the application
2. Navigate to each page
3. Test all interactive features
4. Verify data exports
5. Check error handling

### Validation Checklist
- ✅ All pages load without errors
- ✅ API calls work or fallback gracefully
- ✅ Tables display and paginate correctly
- ✅ Filters apply as expected
- ✅ Exports generate valid files
- ✅ Visualizations render properly

## 🎯 Production Features

### Performance
- Efficient caching mechanism
- Pagination for large datasets
- Optimized data structures
- Lazy loading

### Security
- Input validation
- Error handling
- Timeout management
- Safe data serialization

### User Experience
- Loading indicators
- Clear error messages
- Intuitive navigation
- Responsive design
- Fallback mechanisms

### Maintainability
- Modular architecture
- Clear documentation
- Type hints
- Consistent naming
- Reusable components

## 🔄 Backend Integration

This frontend is designed to work with a REST API backend. Expected API endpoints:

- `GET /api/v1/kpi/overview` - KPI overview data
- `GET /api/v1/reports/list` - Available reports
- `GET /api/v1/reports/{report_id}` - Report data
- `GET /api/v1/kpi/timeseries` - Time series data
- `GET /api/v1/kpi/compare` - Period comparison
- `GET /api/v1/kpi/top-performers` - Top performers

If backend is unavailable, the application uses realistic sample data.

## 📈 Future Enhancements

Potential improvements:
- Real-time data streaming
- Advanced analytics (ML/AI)
- Custom dashboard builder
- Scheduled reports
- Email integration
- Multi-user authentication
- Mobile app
- Dark mode

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

[Add your license information here]

## 📞 Support

For questions or issues:
1. Check [FEATURES.md](FEATURES.md) for detailed documentation
2. Review inline code comments
3. Check error messages in the UI

## ✨ New in This Release

### Version 2.1 (May 2026) - Latest
- ✅ **Loading States** - Production-level loading indicators
- ✅ **Error Handling** - Comprehensive error management system
- ✅ **User Feedback** - Clear loading and error messages
- ✅ **Retry Mechanisms** - Automatic retry for transient errors
- ✅ **Error Recovery** - Actionable suggestions for users
- ✅ **Status Tracking** - API call status monitoring

### Version 2.0 (May 2026)
- ✅ **Enhanced API Service** - Comprehensive KPI endpoints
- ✅ **Interactive Tables** - Advanced filtering and export
- ✅ **Reports Page** - Multiple report types
- ✅ **Export Utilities** - Multi-format data export
- ✅ **Data Processing** - Complete transformation suite
- ✅ **Production Ready** - Enterprise-level code quality

---

**Built with ❤️ using Streamlit**

*Last Updated: May 11, 2026*