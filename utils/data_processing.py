"""
Data Processing Utilities

Production-level utilities for data transformation and processing:
- Data cleaning and normalization
- Type conversions
- Date handling
- Aggregation helpers
- KPI calculations
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any, Union, Tuple
import re


class DataCleaner:
    """
    Data cleaning and normalization utilities.
    """
    
    @staticmethod
    def clean_column_names(data: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and standardize column names.
        - Convert to lowercase
        - Replace spaces with underscores
        - Remove special characters
        
        Args:
            data: DataFrame with columns to clean
        
        Returns:
            DataFrame with cleaned column names
        """
        df = data.copy()
        df.columns = [
            re.sub(r'[^\w\s]', '', col)  # Remove special chars
            .lower()  # Lowercase
            .strip()  # Trim whitespace
            .replace(' ', '_')  # Replace spaces
            for col in df.columns
        ]
        return df
    
    @staticmethod
    def remove_duplicates(
        data: pd.DataFrame,
        subset: Optional[List[str]] = None,
        keep: str = 'first'
    ) -> pd.DataFrame:
        """
        Remove duplicate rows.
        
        Args:
            data: DataFrame to clean
            subset: Columns to consider for duplicates
            keep: Which duplicates to keep ('first', 'last', False)
        
        Returns:
            DataFrame without duplicates
        """
        return data.drop_duplicates(subset=subset, keep=keep)
    
    @staticmethod
    def handle_missing_values(
        data: pd.DataFrame,
        strategy: str = 'drop',
        fill_value: Any = None,
        columns: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Handle missing values in DataFrame.
        
        Args:
            data: DataFrame to process
            strategy: 'drop', 'fill', 'forward', 'backward', 'mean', 'median'
            fill_value: Value to use for 'fill' strategy
            columns: Specific columns to process (None = all)
        
        Returns:
            DataFrame with missing values handled
        """
        df = data.copy()
        target_cols = columns if columns else df.columns
        
        if strategy == 'drop':
            df = df.dropna(subset=target_cols)
        
        elif strategy == 'fill':
            df[target_cols] = df[target_cols].fillna(fill_value)
        
        elif strategy == 'forward':
            df[target_cols] = df[target_cols].fillna(method='ffill')
        
        elif strategy == 'backward':
            df[target_cols] = df[target_cols].fillna(method='bfill')
        
        elif strategy == 'mean':
            for col in target_cols:
                if df[col].dtype in ['int64', 'float64']:
                    df[col] = df[col].fillna(df[col].mean())
        
        elif strategy == 'median':
            for col in target_cols:
                if df[col].dtype in ['int64', 'float64']:
                    df[col] = df[col].fillna(df[col].median())
        
        return df
    
    @staticmethod
    def remove_outliers(
        data: pd.DataFrame,
        columns: List[str],
        method: str = 'iqr',
        threshold: float = 1.5
    ) -> pd.DataFrame:
        """
        Remove outliers from numeric columns.
        
        Args:
            data: DataFrame to process
            columns: Columns to check for outliers
            method: 'iqr' or 'zscore'
            threshold: Threshold for outlier detection (IQR multiplier or z-score)
        
        Returns:
            DataFrame with outliers removed
        """
        df = data.copy()
        
        for col in columns:
            if col not in df.columns or df[col].dtype not in ['int64', 'float64']:
                continue
            
            if method == 'iqr':
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - threshold * IQR
                upper_bound = Q3 + threshold * IQR
                df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
            
            elif method == 'zscore':
                z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
                df = df[z_scores < threshold]
        
        return df


class DataTransformer:
    """
    Data transformation and feature engineering utilities.
    """
    
    @staticmethod
    def convert_date_columns(
        data: pd.DataFrame,
        date_columns: List[str],
        format: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Convert columns to datetime type.
        
        Args:
            data: DataFrame to process
            date_columns: Columns to convert
            format: Date format string (auto-detect if None)
        
        Returns:
            DataFrame with converted date columns
        """
        df = data.copy()
        
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], format=format, errors='coerce')
        
        return df
    
    @staticmethod
    def extract_date_features(
        data: pd.DataFrame,
        date_column: str,
        features: List[str] = ['year', 'month', 'day', 'dayofweek', 'quarter']
    ) -> pd.DataFrame:
        """
        Extract date features from datetime column.
        
        Args:
            data: DataFrame to process
            date_column: Column containing datetime values
            features: Features to extract
        
        Returns:
            DataFrame with additional date feature columns
        """
        df = data.copy()
        
        if date_column not in df.columns:
            return df
        
        # Ensure datetime type
        if df[date_column].dtype != 'datetime64[ns]':
            df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
        
        # Extract features
        if 'year' in features:
            df[f'{date_column}_year'] = df[date_column].dt.year
        
        if 'month' in features:
            df[f'{date_column}_month'] = df[date_column].dt.month
        
        if 'day' in features:
            df[f'{date_column}_day'] = df[date_column].dt.day
        
        if 'dayofweek' in features:
            df[f'{date_column}_dayofweek'] = df[date_column].dt.dayofweek
        
        if 'quarter' in features:
            df[f'{date_column}_quarter'] = df[date_column].dt.quarter
        
        if 'week' in features:
            df[f'{date_column}_week'] = df[date_column].dt.isocalendar().week
        
        if 'is_weekend' in features:
            df[f'{date_column}_is_weekend'] = df[date_column].dt.dayofweek.isin([5, 6])
        
        return df
    
    @staticmethod
    def create_bins(
        data: pd.DataFrame,
        column: str,
        bins: Union[int, List[float]],
        labels: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Create binned categories from numeric column.
        
        Args:
            data: DataFrame to process
            column: Column to bin
            bins: Number of bins or bin edges
            labels: Labels for bins
        
        Returns:
            DataFrame with new binned column
        """
        df = data.copy()
        
        if column not in df.columns:
            return df
        
        df[f'{column}_bin'] = pd.cut(df[column], bins=bins, labels=labels)
        
        return df
    
    @staticmethod
    def normalize_numeric_columns(
        data: pd.DataFrame,
        columns: Optional[List[str]] = None,
        method: str = 'minmax'
    ) -> pd.DataFrame:
        """
        Normalize numeric columns.
        
        Args:
            data: DataFrame to process
            columns: Columns to normalize (None = all numeric)
            method: 'minmax' or 'zscore'
        
        Returns:
            DataFrame with normalized columns
        """
        df = data.copy()
        
        if columns is None:
            columns = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        
        for col in columns:
            if col not in df.columns or df[col].dtype not in ['int64', 'float64']:
                continue
            
            if method == 'minmax':
                min_val = df[col].min()
                max_val = df[col].max()
                df[f'{col}_normalized'] = (df[col] - min_val) / (max_val - min_val)
            
            elif method == 'zscore':
                mean = df[col].mean()
                std = df[col].std()
                df[f'{col}_normalized'] = (df[col] - mean) / std
        
        return df


class KPICalculator:
    """
    Business KPI calculation utilities.
    """
    
    @staticmethod
    def calculate_growth_rate(
        current_value: float,
        previous_value: float
    ) -> float:
        """
        Calculate growth rate between two values.
        
        Args:
            current_value: Current period value
            previous_value: Previous period value
        
        Returns:
            Growth rate as percentage
        """
        if previous_value == 0:
            return 0.0
        
        return ((current_value - previous_value) / previous_value) * 100
    
    @staticmethod
    def calculate_moving_average(
        data: pd.Series,
        window: int = 7
    ) -> pd.Series:
        """
        Calculate moving average.
        
        Args:
            data: Time series data
            window: Window size for moving average
        
        Returns:
            Moving average series
        """
        return data.rolling(window=window, min_periods=1).mean()
    
    @staticmethod
    def calculate_customer_metrics(
        data: pd.DataFrame,
        customer_col: str = 'customer_id',
        revenue_col: str = 'revenue',
        date_col: str = 'date'
    ) -> pd.DataFrame:
        """
        Calculate customer-level KPI metrics.
        
        Args:
            data: Transaction data
            customer_col: Customer identifier column
            revenue_col: Revenue column
            date_col: Date column
        
        Returns:
            DataFrame with customer metrics
        """
        df = data.copy()
        
        # Ensure date is datetime
        if df[date_col].dtype != 'datetime64[ns]':
            df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        
        customer_metrics = df.groupby(customer_col).agg({
            revenue_col: ['sum', 'mean', 'count'],
            date_col: ['min', 'max']
        }).reset_index()
        
        # Flatten column names
        customer_metrics.columns = [
            f'{col[0]}_{col[1]}' if col[1] else col[0]
            for col in customer_metrics.columns
        ]
        
        # Rename for clarity
        customer_metrics = customer_metrics.rename(columns={
            f'{revenue_col}_sum': 'lifetime_value',
            f'{revenue_col}_mean': 'average_order_value',
            f'{revenue_col}_count': 'total_orders',
            f'{date_col}_min': 'first_purchase',
            f'{date_col}_max': 'last_purchase'
        })
        
        # Calculate days since last purchase
        customer_metrics['days_since_last_purchase'] = (
            datetime.now() - customer_metrics['last_purchase']
        ).dt.days
        
        # Calculate customer lifetime (days)
        customer_metrics['customer_lifetime_days'] = (
            customer_metrics['last_purchase'] - customer_metrics['first_purchase']
        ).dt.days
        
        return customer_metrics
    
    @staticmethod
    def calculate_product_metrics(
        data: pd.DataFrame,
        product_col: str = 'product_id',
        revenue_col: str = 'revenue',
        quantity_col: str = 'quantity',
        cost_col: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Calculate product-level KPI metrics.
        
        Args:
            data: Transaction data
            product_col: Product identifier column
            revenue_col: Revenue column
            quantity_col: Quantity sold column
            cost_col: Cost column (optional)
        
        Returns:
            DataFrame with product metrics
        """
        df = data.copy()
        
        agg_dict = {
            revenue_col: ['sum', 'mean'],
            quantity_col: 'sum'
        }
        
        if cost_col and cost_col in df.columns:
            agg_dict[cost_col] = 'sum'
        
        product_metrics = df.groupby(product_col).agg(agg_dict).reset_index()
        
        # Flatten column names
        product_metrics.columns = [
            f'{col[0]}_{col[1]}' if isinstance(col, tuple) and col[1] else col[0]
            for col in product_metrics.columns
        ]
        
        # Rename for clarity
        rename_dict = {
            f'{revenue_col}_sum': 'total_revenue',
            f'{revenue_col}_mean': 'average_price',
            f'{quantity_col}_sum': 'total_units_sold'
        }
        
        if cost_col:
            rename_dict[f'{cost_col}_sum'] = 'total_cost'
        
        product_metrics = product_metrics.rename(columns=rename_dict)
        
        # Calculate profit if cost is available
        if cost_col and cost_col in df.columns:
            product_metrics['total_profit'] = (
                product_metrics['total_revenue'] - product_metrics['total_cost']
            )
            product_metrics['profit_margin'] = (
                product_metrics['total_profit'] / product_metrics['total_revenue'] * 100
            ).round(2)
        
        return product_metrics
    
    @staticmethod
    def calculate_time_series_metrics(
        data: pd.DataFrame,
        date_col: str,
        metric_col: str,
        aggregation: str = 'sum',
        frequency: str = 'D'
    ) -> pd.DataFrame:
        """
        Calculate time series metrics with trend analysis.
        
        Args:
            data: Transaction data
            date_col: Date column
            metric_col: Metric to aggregate
            aggregation: Aggregation function ('sum', 'mean', 'count')
            frequency: Time frequency ('D'=daily, 'W'=weekly, 'M'=monthly)
        
        Returns:
            DataFrame with time series metrics and trends
        """
        df = data.copy()
        
        # Ensure date is datetime
        if df[date_col].dtype != 'datetime64[ns]':
            df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        
        # Set date as index and resample
        df = df.set_index(date_col)
        
        if aggregation == 'sum':
            time_series = df[metric_col].resample(frequency).sum().reset_index()
        elif aggregation == 'mean':
            time_series = df[metric_col].resample(frequency).mean().reset_index()
        elif aggregation == 'count':
            time_series = df[metric_col].resample(frequency).count().reset_index()
        
        # Calculate moving averages
        time_series['ma_7'] = time_series[metric_col].rolling(window=7, min_periods=1).mean()
        time_series['ma_30'] = time_series[metric_col].rolling(window=30, min_periods=1).mean()
        
        # Calculate period-over-period change
        time_series['pop_change'] = time_series[metric_col].pct_change() * 100
        
        return time_series


class DataAggregator:
    """
    Utilities for data aggregation and summarization.
    """
    
    @staticmethod
    def aggregate_by_dimension(
        data: pd.DataFrame,
        dimension: str,
        metrics: Dict[str, str],
        sort_by: Optional[str] = None,
        ascending: bool = False,
        top_n: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Aggregate data by a dimension.
        
        Args:
            data: DataFrame to aggregate
            dimension: Column to group by
            metrics: Dictionary mapping column names to aggregation functions
            sort_by: Column to sort by
            ascending: Sort order
            top_n: Return only top N rows
        
        Returns:
            Aggregated DataFrame
        """
        result = data.groupby(dimension).agg(metrics).reset_index()
        
        # Flatten multi-index columns if needed
        if isinstance(result.columns, pd.MultiIndex):
            result.columns = ['_'.join(col).strip('_') for col in result.columns.values]
        
        # Sort if specified
        if sort_by:
            result = result.sort_values(sort_by, ascending=ascending)
        
        # Limit to top N
        if top_n:
            result = result.head(top_n)
        
        return result
    
    @staticmethod
    def create_summary_table(
        data: pd.DataFrame,
        group_by: List[str],
        agg_columns: Dict[str, List[str]]
    ) -> pd.DataFrame:
        """
        Create multi-level summary table.
        
        Args:
            data: DataFrame to summarize
            group_by: Columns to group by
            agg_columns: Dictionary mapping columns to aggregation functions
        
        Returns:
            Summary DataFrame
        """
        summary = data.groupby(group_by).agg(agg_columns).reset_index()
        
        # Flatten column names
        if isinstance(summary.columns, pd.MultiIndex):
            summary.columns = [
                '_'.join(col).strip('_') if isinstance(col, tuple) else col
                for col in summary.columns.values
            ]
        
        return summary
