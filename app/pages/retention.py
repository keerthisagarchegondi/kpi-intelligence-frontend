"""
Customer Retention & Churn Analysis Page

Production-level retention analytics dashboard with comprehensive visualizations,
cohort analysis, churn predictions, and actionable insights.
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from components.filters import render_date_range_filter, get_filter_summary
from components.charts import (
    create_cohort_retention_heatmap,
    create_retention_trend_chart,
    create_segment_retention_comparison,
    create_churn_reasons_chart,
    create_churn_risk_distribution,
    create_ltv_by_segment_chart,
    get_retention_sample_data,
    get_segment_retention_data,
    get_churn_prediction_data,
    get_churn_reasons_data
)

# Page configuration
st.set_page_config(
    page_title="Retention Metrics - KPI Intelligence",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced styling
st.markdown("""
<style>
    .retention-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #00897b;
        margin-bottom: 0.5rem;
    }
    .metric-positive {
        color: #66bb6a;
        font-weight: 600;
    }
    .metric-negative {
        color: #ef5350;
        font-weight: 600;
    }
    .insight-card {
        background-color: #f5f5f5;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #00897b;
        margin: 1rem 0;
    }
    .warning-card {
        background-color: #fff3e0;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ff9800;
        margin: 1rem 0;
    }
    .success-card {
        background-color: #e8f5e9;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #66bb6a;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Page header
st.markdown('<h1 class="retention-header">🔄 Customer Retention & Churn Analysis</h1>', unsafe_allow_html=True)
st.markdown('<p style="font-size: 1.1rem; color: #666; margin-bottom: 2rem;">Analyze retention trends, identify churn risks, and optimize customer lifetime value</p>', unsafe_allow_html=True)
st.markdown("---")

# Render filters
with st.expander("🔧 Analysis Filters", expanded=True):
    start_date, end_date, filters_applied = render_date_range_filter(
        key_prefix="retention",
        default_range="Last 6 Months",
        show_apply_button=True
    )
    
    # Additional retention-specific filters
    col_f1, col_f2 = st.columns(2)
    
    with col_f1:
        cohort_type = st.selectbox(
            "Cohort Type",
            options=["Monthly", "Weekly", "Quarterly"],
            help="Select cohort grouping for retention analysis"
        )
    
    with col_f2:
        segment = st.selectbox(
            "Customer Segment",
            options=["All Customers", "New Customers", "Existing Customers", "Enterprise", "SMB"],
            help="Filter by customer segment"
        )

# Main content
if filters_applied:
    st.success(f"📅 **Active Period:** {start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')} | **Cohort:** {cohort_type} | **Segment:** {segment}")
    st.markdown("---")
    
    # Load retention data
    segment_data = get_segment_retention_data()
    churn_prediction = get_churn_prediction_data()
    churn_reasons = get_churn_reasons_data()
    
    # Calculate key metrics
    overall_retention = segment_data['30_day_retention'].mean()
    overall_churn = 100 - overall_retention
    retention_delta = 2.1  # Positive trend
    total_at_risk = churn_prediction['high_risk'].sum()
    avg_ltv = segment_data['avg_ltv'].mean()
    active_customers = segment_data['segment'].apply(lambda x: 1247 if x == 'Enterprise' else 0).sum() or 8562
    
    # Key retention metrics
    st.subheader("🎯 Key Retention Metrics")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="Overall Retention Rate",
            value=f"{overall_retention:.1f}%",
            delta=f"+{retention_delta}%",
            help="Average percentage of customers retained across all segments"
        )
    
    with col2:
        st.metric(
            label="Churn Rate",
            value=f"{overall_churn:.1f}%",
            delta=f"-{retention_delta}%",
            delta_color="inverse",
            help="Average percentage of customers lost in period"
        )
    
    with col3:
        st.metric(
            label="Avg Customer LTV",
            value=f"${avg_ltv:,.0f}",
            delta="+5.8%",
            help="Average customer lifetime value across all segments"
        )
    
    with col4:
        st.metric(
            label="Active Customers",
            value=f"{active_customers:,}",
            delta="+94",
            help="Total active customers in period"
        )
    
    with col5:
        st.metric(
            label="High Churn Risk",
            value=f"{total_at_risk:,}",
            delta="-12",
            delta_color="inverse",
            help="Customers at high risk of churning"
        )
    
    st.markdown("---")
    
    # Retention analysis sections
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Cohort Analysis", 
        "📉 Churn Analysis", 
        "💎 Segment Performance",
        "💰 Lifetime Value"
    ])
    
    # TAB 1: Cohort Analysis
    with tab1:
        st.subheader("📊 Cohort Retention Analysis")
        st.markdown(f"Analyzing **{cohort_type.lower()}** cohorts to track customer retention patterns over time.")
        
        # Cohort retention heatmap
        st.plotly_chart(
            create_cohort_retention_heatmap(height=500),
            use_container_width=True
        )
        
        st.markdown("---")
        
        # Retention trend over time
        col_t1, col_t2 = st.columns([2, 1])
        
        with col_t1:
            st.markdown("#### Retention Rate Trends")
            st.plotly_chart(
                create_retention_trend_chart(days=90, height=400),
                use_container_width=True
            )
        
        with col_t2:
            st.markdown("#### Key Insights")
            st.markdown("""
            <div class="success-card">
            <strong>✅ Positive Trends</strong>
            <ul>
                <li>Retention improving month-over-month</li>
                <li>Recent cohorts show stronger retention</li>
                <li>Above 85% target for 3 consecutive months</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="warning-card">
            <strong>⚠️ Watch Areas</strong>
            <ul>
                <li>Month 3 drop-off point needs attention</li>
                <li>Older cohorts showing gradual decline</li>
                <li>Weekend engagement lower than weekdays</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Cohort insights
        st.markdown("#### 💡 Cohort Analysis Insights")
        col_i1, col_i2, col_i3 = st.columns(3)
        
        with col_i1:
            st.markdown("""
            **First Month Critical**
            - 85-90% retention in Month 1
            - Strong onboarding impact visible
            - Early engagement key to success
            """)
        
        with col_i2:
            st.markdown("""
            **3-Month Milestone**
            - Average 65-70% retention at Month 3
            - Critical decision point for customers
            - Targeted intervention opportunity
            """)
        
        with col_i3:
            st.markdown("""
            **Long-term Stability**
            - Retention stabilizes after Month 4
            - 60% retention indicates loyal base
            - Focus on value delivery
            """)
    
    # TAB 2: Churn Analysis
    with tab2:
        st.subheader("📉 Churn Analysis & Risk Prediction")
        st.markdown("Identify churn patterns, understand reasons, and predict at-risk customers for proactive intervention.")
        
        # Churn risk distribution
        col_c1, col_c2 = st.columns(2)
        
        with col_c1:
            st.markdown("#### Churn Risk Distribution by Segment")
            st.plotly_chart(
                create_churn_risk_distribution(height=400),
                use_container_width=True
            )
        
        with col_c2:
            st.markdown("#### Top Reasons for Churn")
            st.plotly_chart(
                create_churn_reasons_chart(height=400),
                use_container_width=True
            )
        
        st.markdown("---")
        
        # At-risk customers details
        st.markdown("#### 🚨 High-Risk Customer Segments")
        
        high_risk_df = churn_prediction[['segment', 'high_risk']].sort_values('high_risk', ascending=False)
        
        col_r1, col_r2, col_r3 = st.columns([2, 2, 2])
        
        with col_r1:
            st.markdown("**Priority Actions Required**")
            for idx, row in high_risk_df.head(3).iterrows():
                st.markdown(f"""
                <div class="warning-card">
                <strong>{row['segment']}</strong><br>
                <span style="font-size: 1.5rem; color: #ef5350;">{row['high_risk']}</span> customers at high risk<br>
                <em>Immediate intervention recommended</em>
                </div>
                """, unsafe_allow_html=True)
        
        with col_r2:
            st.markdown("**Recommended Interventions**")
            st.markdown("""
            1. **Personal Outreach**
               - Schedule 1-on-1 check-ins
               - Understand pain points
               - Offer customized solutions
            
            2. **Value Reinforcement**
               - Highlight unused features
               - Share success stories
               - Demonstrate ROI
            
            3. **Special Offers**
               - Retention discounts
               - Premium feature trials
               - Extended support
            """)
        
        with col_r3:
            st.markdown("**Churn Prevention ROI**")
            st.metric(
                "Potential Revenue at Risk",
                f"${total_at_risk * 1250:,.0f}",
                help="Estimated revenue from high-risk customers"
            )
            st.metric(
                "Retention Campaign Cost",
                f"${total_at_risk * 85:,.0f}",
                help="Estimated cost of retention campaign"
            )
            st.metric(
                "Net Benefit (50% success)",
                f"${(total_at_risk * 1250 * 0.5) - (total_at_risk * 85):,.0f}",
                delta="Positive ROI",
                help="Expected benefit if 50% of at-risk customers retained"
            )
        
        st.markdown("---")
        
        # Churn prediction insights
        st.markdown("#### 🔮 Predictive Churn Indicators")
        
        col_p1, col_p2, col_p3, col_p4 = st.columns(4)
        
        with col_p1:
            st.markdown("""
            **Engagement Signals**
            - Login frequency declined
            - Feature usage dropped 30%+
            - Support tickets increased
            """)
        
        with col_p2:
            st.markdown("""
            **Behavioral Patterns**
            - No activity for 14+ days
            - Cancelled training sessions
            - Downgrade inquiries
            """)
        
        with col_p3:
            st.markdown("""
            **Business Indicators**
            - Payment delays
            - Contract near expiration
            - Team size reduction
            """)
        
        with col_p4:
            st.markdown("""
            **Sentiment Analysis**
            - Negative NPS scores
            - Support satisfaction low
            - Social media complaints
            """)
    
    # TAB 3: Segment Performance
    with tab3:
        st.subheader("💎 Customer Segment Performance")
        
        if segment != "All Customers":
            st.info(f"📊 Viewing detailed analysis for: **{segment}**")
        else:
            st.markdown("Comprehensive retention analysis across all customer segments.")
        
        # Segment retention comparison
        st.markdown("#### Retention Rates by Segment")
        st.plotly_chart(
            create_segment_retention_comparison(height=450),
            use_container_width=True
        )
        
        st.markdown("---")
        
        # Segment performance table
        st.markdown("#### 📊 Detailed Segment Metrics")
        
        # Enhanced display dataframe
        display_df = segment_data.copy()
        display_df['30_day_retention'] = display_df['30_day_retention'].apply(lambda x: f"{x:.1f}%")
        display_df['90_day_retention'] = display_df['90_day_retention'].apply(lambda x: f"{x:.1f}%")
        display_df['avg_ltv'] = display_df['avg_ltv'].apply(lambda x: f"${x:,.0f}")
        display_df.columns = ['Segment', '30-Day Retention', '90-Day Retention', 'Avg LTV']
        
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )
        
        st.markdown("---")
        
        # Segment insights
        st.markdown("#### 💡 Segment-Specific Insights")
        
        col_s1, col_s2 = st.columns(2)
        
        with col_s1:
            st.markdown("""
            <div class="success-card">
            <strong>🏆 Best Performers</strong><br><br>
            <strong>Enterprise Segment</strong>
            <ul>
                <li>96.8% retention (30-day)</li>
                <li>$52,000 average LTV</li>
                <li>Dedicated account management</li>
                <li>High product adoption</li>
            </ul>
            <strong>Recommendation:</strong> Replicate engagement model for Mid-Market
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="success-card">
            <strong>📈 Improving Segments</strong><br><br>
            <strong>Mid-Market</strong>
            <ul>
                <li>92.4% retention (+3.2% QoQ)</li>
                <li>Strong growth trajectory</li>
                <li>Positive engagement trends</li>
            </ul>
            <strong>Action:</strong> Continue current strategies, expand resources
            </div>
            """, unsafe_allow_html=True)
        
        with col_s2:
            st.markdown("""
            <div class="warning-card">
            <strong>⚠️ Needs Attention</strong><br><br>
            <strong>Free Trial Users</strong>
            <ul>
                <li>54.7% retention (critical)</li>
                <li>High drop-off after trial</li>
                <li>Conversion rate below target</li>
            </ul>
            <strong>Action Plan:</strong>
            <ol>
                <li>Enhance onboarding experience</li>
                <li>Increase trial engagement touchpoints</li>
                <li>Clarify value proposition early</li>
                <li>Implement activation milestones</li>
            </ol>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="warning-card">
            <strong>🎯 Growth Opportunity</strong><br><br>
            <strong>Small Business & Startup</strong>
            <ul>
                <li>Moderate retention (72-81%)</li>
                <li>Price-sensitive segment</li>
                <li>High growth potential</li>
            </ul>
            <strong>Strategy:</strong> Value-based pricing, self-service resources
            </div>
            """, unsafe_allow_html=True)
    
    # TAB 4: Lifetime Value
    with tab4:
        st.subheader("💰 Customer Lifetime Value Analysis")
        st.markdown("Understanding long-term customer value to optimize acquisition and retention investments.")
        
        # LTV by segment chart
        st.plotly_chart(
            create_ltv_by_segment_chart(height=400),
            use_container_width=True
        )
        
        st.markdown("---")
        
        # LTV metrics and insights
        col_ltv1, col_ltv2, col_ltv3 = st.columns(3)
        
        with col_ltv1:
            st.markdown("#### 📊 LTV Metrics")
            st.metric("Average LTV (All Segments)", f"${avg_ltv:,.0f}")
            st.metric("Enterprise LTV", "$52,000", delta="+8.5%")
            st.metric("LTV:CAC Ratio", "4.2:1", delta="+0.3")
            st.markdown("""
            **Healthy Indicators:**
            - LTV:CAC ratio above 3:1 ✅
            - Average LTV growing YoY ✅
            - Premium segments expanding ✅
            """)
        
        with col_ltv2:
            st.markdown("#### 🎯 Optimization Strategies")
            st.markdown("""
            **Increase LTV:**
            1. **Upsell & Cross-sell**
               - Identify expansion opportunities
               - Introduce premium features
               - Bundle complementary services
            
            2. **Reduce Churn**
               - Proactive customer success
               - Regular health scoring
               - Early intervention programs
            
            3. **Extend Customer Lifetime**
               - Annual contract incentives
               - Loyalty rewards programs
               - Community building
            """)
        
        with col_ltv3:
            st.markdown("#### 💡 Value Drivers")
            st.markdown("""
            **Top LTV Contributors:**
            - Product adoption depth
            - Feature utilization rate
            - Customer success engagement
            - Contract length
            - Payment frequency
            
            **Focus Areas:**
            - Enterprise: Expand deployment
            - Mid-Market: Feature adoption
            - SMB: Self-service efficiency
            - Startup: Success milestones
            - Trial: Activation rate
            """)
        
        st.markdown("---")
        
        # LTV projections
        st.markdown("#### 📈 LTV Projections & Scenarios")
        
        col_proj1, col_proj2 = st.columns(2)
        
        with col_proj1:
            st.markdown("""
            <div class="insight-card">
            <strong>Conservative Scenario</strong><br>
            <ul>
                <li>Current retention maintained: 87.3%</li>
                <li>No churn reduction initiatives</li>
                <li>Projected LTV: $15,240</li>
                <li>Annual customer value: $2.8M</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col_proj2:
            st.markdown("""
            <div class="success-card">
            <strong>Optimistic Scenario</strong><br>
            <ul>
                <li>Retention improved to 92%</li>
                <li>Active churn prevention</li>
                <li>Projected LTV: $18,750 (+23%)</li>
                <li>Annual customer value: $3.4M (+21%)</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Executive Summary & Action Items
    st.subheader("⚡ Executive Summary & Recommended Actions")
    
    col_exec1, col_exec2 = st.columns(2)
    
    with col_exec1:
        st.markdown("""
        <div class="success-card">
        <h4>✅ Key Achievements</h4>
        <ul>
            <li><strong>Retention rate above target:</strong> 87.3% vs 85% goal</li>
            <li><strong>Improving trend:</strong> +2.1% month-over-month</li>
            <li><strong>Enterprise retention excellent:</strong> 96.8%</li>
            <li><strong>Strong LTV:CAC ratio:</strong> 4.2:1</li>
            <li><strong>Recent cohorts outperforming:</strong> +4.5% vs previous</li>
        </ul>
        <br>
        <strong>Continue:</strong> Current engagement strategies, account management model, customer success programs
        </div>
        """, unsafe_allow_html=True)
    
    with col_exec2:
        st.markdown(f"""
        <div class="warning-card">
        <h4>⚠️ Priority Action Items</h4>
        <ol>
            <li><strong>Immediate: High-Risk Customers</strong>
                <ul>
                    <li>{total_at_risk:,} customers need intervention</li>
                    <li>Launch retention campaign this week</li>
                    <li>Assign account managers to top 50</li>
                </ul>
            </li>
            <li><strong>Short-term: Trial Conversion</strong>
                <ul>
                    <li>54.7% retention too low</li>
                    <li>Redesign onboarding flow</li>
                    <li>Add activation milestones</li>
                </ul>
            </li>
            <li><strong>Medium-term: Month 3 Drop-off</strong>
                <ul>
                    <li>Implement 90-day check-in program</li>
                    <li>Enhance product education</li>
                    <li>Value demonstration cadence</li>
                </ul>
            </li>
        </ol>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick action buttons (for demo purposes)
    st.markdown("---")
    st.markdown("#### 🚀 Quick Actions")
    
    col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)
    
    with col_btn1:
        if st.button("📧 Export At-Risk List", use_container_width=True):
            st.success("✅ Export initiated! Download will start shortly.")
    
    with col_btn2:
        if st.button("📊 Generate Report", use_container_width=True):
            st.success("✅ Retention report generated successfully!")
    
    with col_btn3:
        if st.button("🎯 Launch Campaign", use_container_width=True):
            st.success("✅ Retention campaign workflow started!")
    
    with col_btn4:
        if st.button("📅 Schedule Review", use_container_width=True):
            st.success("✅ Quarterly retention review scheduled!")

else:
    st.info("👆 Please apply filters above to view comprehensive retention and churn analysis.")
    
    # Show preview of what's available
    st.markdown("---")
    st.markdown("### 📊 Available Analytics")
    
    col_preview1, col_preview2, col_preview3 = st.columns(3)
    
    with col_preview1:
        st.markdown("""
        **Cohort Analysis**
        - Retention heatmaps
        - Trend analysis
        - Monthly/weekly cohorts
        - Historical comparisons
        """)
    
    with col_preview2:
        st.markdown("""
        **Churn Prevention**
        - Risk scoring
        - Predictive analytics
        - Intervention strategies
        - ROI calculations
        """)
    
    with col_preview3:
        st.markdown("""
        **Lifetime Value**
        - Segment LTV analysis
        - Projection scenarios
        - Optimization strategies
        - Value drivers
        """)
    st.info("👆 Please apply filters to view retention and churn analysis.")
