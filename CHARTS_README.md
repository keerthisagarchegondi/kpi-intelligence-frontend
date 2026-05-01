# Charts Component - Production-Level Sample Data

## Overview

The `components/charts.py` module now includes **production-level static sample data** for all chart types. All sample data is realistic, follows business patterns, and is perfect for development, testing, and demonstrations.

## Key Features

✅ **Realistic Business Data** - All sample data reflects actual business patterns  
✅ **Weekly Seasonality** - Weekday vs weekend patterns  
✅ **Growth Trends** - Realistic growth trajectories  
✅ **Business Context** - Revenue, costs, customers, regions, channels, products  
✅ **Production Ready** - No random data, consistent and reproducible  
✅ **Zero Configuration** - Charts work immediately without any data  

## Available Chart Types

### 1. **Line Charts**
- Single and multi-series time trends
- Realistic revenue, cost, and profit patterns
- Weekly seasonality and growth trends

### 2. **Bar Charts**
- Vertical and horizontal layouts
- Product performance data
- Marketing channel comparisons
- Follows Pareto distribution (80/20 rule)

### 3. **Pie/Donut Charts**
- Customer segmentation by revenue
- Realistic segment distributions
- Enterprise, Mid-Market, Small Business, etc.

### 4. **Gauge & Indicators**
- KPI monitoring with realistic ranges
- Customer satisfaction scores (60-95%)
- Revenue metrics with MoM growth
- Context-aware value generation

### 5. **Heatmaps**
- User activity patterns by day/hour
- Peak business hours (weekdays 9am-6pm)
- Reduced weekend activity

### 6. **Combo Charts**
- Revenue bars with growth rate lines
- Dual y-axes for different scales
- 12-month business data

## Sample Data Functions

### Business KPI Data
```python
get_revenue_sample_data(period='30d')      # Revenue, cost, profit by period
get_customer_segmentation_data()            # Segments, customers, churn
get_product_performance_data()              # Products, revenue, growth
get_channel_performance_data()              # Marketing channels, ROI
get_regional_performance_data()             # Geographic performance
get_daily_metrics_data(days=30)            # Operational metrics
get_retention_sample_data()                # Cohort retention data
```

### Convenience Demo Functions
```python
create_revenue_trend_chart(period='30d')
create_revenue_breakdown_chart(period='12m')
create_product_revenue_chart(orientation='v')
create_segment_revenue_chart()
create_channel_performance_chart()
create_regional_performance_chart()
create_activity_heatmap_chart()
create_customer_satisfaction_gauge()
create_mrr_indicator()
create_revenue_growth_combo_chart()
```

## Usage Examples

### Basic Usage (Auto Sample Data)
```python
import streamlit as st
from components.charts import create_revenue_trend_chart

# Uses built-in sample data automatically
fig = create_revenue_trend_chart(period='30d')
st.plotly_chart(fig, use_container_width=True)
```

### Custom Data
```python
import streamlit as st
from components.charts import create_line_chart
import pandas as pd

# Use your own data
your_data = pd.DataFrame({
    'date': [...],
    'revenue': [...]
})

fig = create_line_chart(
    data=your_data,
    x_column='date',
    y_column='revenue',
    title='My Revenue Trend'
)
st.plotly_chart(fig, use_container_width=True)
```

### Get All Sample Charts
```python
from components.charts import get_all_sample_charts

# Get dictionary of all pre-configured charts
charts = get_all_sample_charts()
st.plotly_chart(charts['revenue_trend'])
st.plotly_chart(charts['product_revenue'])
# ... etc
```

## Sample Data Characteristics

### Revenue Data
- **Base Values**: $12,000 - $15,000 daily revenue
- **Growth Rate**: 2-3% monthly growth
- **Pattern**: 40% lower on weekends
- **Periods**: 30d, 90d, 12m options

### Customer Segmentation
- **Segments**: Enterprise, Mid-Market, Small Business, Startup, Free Trial
- **Distribution**: Follows realistic Pareto pattern
- **Metrics**: Customers, revenue, AOV, churn rate

### Product Performance
- **Products**: 6 product lines with different performance
- **Revenue Range**: $320K - $1.85M per product
- **Growth**: -3.2% to +31.5% realistic variation

### Geographic Data
- **Regions**: 5 major regions (NA, EU, APAC, LATAM, MEA)
- **Distribution**: NA and EU lead, emerging markets growing faster
- **Growth Rates**: 12% - 31% by region

### Activity Patterns
- **Peak Hours**: 9am-6pm weekdays
- **Weekend**: 50-70% reduced activity
- **Time Zones**: Business hours aligned

## Demo Page

A complete demo page is available at:
**`app/pages/charts_demo.py`**

View it by running the app and navigating to the "Charts Demo" page in the sidebar.

Features:
- All chart types with live examples
- Realistic sample data
- Data table views
- Implementation notes
- Copy-paste code examples

## Testing the Charts

Run the Streamlit app:
```bash
streamlit run app/main.py
```

Then navigate to:
- **Charts Demo** page - See all charts with sample data
- Individual pages (Revenue, Dashboard, etc.) to integrate charts

## Data Quality Standards

All sample data meets these standards:
- ✅ **Realistic**: Reflects actual business patterns
- ✅ **Consistent**: Same seed values for reproducibility
- ✅ **Complete**: No missing or null values
- ✅ **Scaled**: Appropriate magnitude for each metric
- ✅ **Balanced**: Follows expected distributions (Pareto, Normal, etc.)

## Next Steps

1. **View the Demo**: Open the Charts Demo page to see all visualizations
2. **Integrate**: Copy chart functions into your dashboard pages
3. **Customize**: Adjust colors, sizes, and labels as needed
4. **Connect**: Replace sample data with your API/database calls
5. **Deploy**: All charts are production-ready

## File Structure

```
components/
  └── charts.py          # Main charts module (1400+ lines)
      ├── Data Generators (realistic business data)
      ├── Chart Functions (all chart types)
      └── Demo Functions (ready-to-use examples)

app/pages/
  └── charts_demo.py     # Complete demo page
```

## Support

For questions or issues:
- See inline documentation in `components/charts.py`
- Review examples in `charts_demo.py`
- Check Plotly documentation: https://plotly.com/python/
- Streamlit documentation: https://docs.streamlit.io/

---

**Status**: ✅ Production Ready  
**Last Updated**: May 2, 2026  
**Sample Data**: Static & Realistic
