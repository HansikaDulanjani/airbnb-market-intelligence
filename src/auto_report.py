import pandas as pd
import numpy as np
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import os

def generate_report():
    print("Generating automated market intelligence report...")

    # Load data
    master = pd.read_csv('data/processed/master_listings.csv', low_memory=False)
    neighbourhood_agg = pd.read_csv('data/processed/neighbourhood_agg.csv')

    # Output path
    os.makedirs('reports', exist_ok=True)
    date_str = datetime.now().strftime('%Y_%m_%d')
    output_path = f'reports/Bangkok_Market_Intelligence_{date_str}.pdf'

    # Document setup
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=24,
        textColor=colors.HexColor('#FF5A5F'),
        spaceAfter=10,
        alignment=TA_CENTER
    )
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.grey,
        spaceAfter=20,
        alignment=TA_CENTER
    )
    heading_style = ParagraphStyle(
        'Heading',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#484848'),
        spaceBefore=20,
        spaceAfter=10
    )
    subheading_style = ParagraphStyle(
        'SubHeading',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=colors.HexColor('#FF5A5F'),
        spaceBefore=15,
        spaceAfter=8
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=8,
        leading=16
    )

    # Content
    content = []

    # TITLE PAGE
    content.append(Spacer(1, 1*inch))
    content.append(Paragraph("Bangkok Airbnb", title_style))
    content.append(Paragraph("Market Intelligence Report", title_style))
    content.append(Spacer(1, 0.3*inch))
    content.append(Paragraph(
        f"Generated: {datetime.now().strftime('%B %d, %Y')}",
        subtitle_style
    ))
    
    content.append(HRFlowable(width="100%", thickness=2,
                               color=colors.HexColor('#FF5A5F')))
    content.append(Spacer(1, 0.5*inch))

    # EXECUTIVE SUMMARY
    content.append(Paragraph("Executive Summary", heading_style))
    content.append(Paragraph(
        f"""This report provides a comprehensive market intelligence analysis of the Bangkok 
        Airbnb market based on Inside Airbnb data scraped in September 2025. 
        The dataset encompasses {master.shape[0]:,} active listings across 
        {master['neighbourhood_cleansed'].nunique()} neighbourhoods, managed by 
        {master['host_id'].nunique():,} unique hosts. Key findings reveal a dynamic 
        short-term rental market with significant price variation across neighbourhoods 
        and strong growth in review volume indicating increasing market demand.""",
        body_style
    ))

    # KPI TABLE
    content.append(Paragraph("Key Market Metrics", subheading_style))
    kpi_data = [
        ['Metric', 'Value'],
        ['Total Listings', f"{master.shape[0]:,}"],
        ['Total Hosts', f"{master['host_id'].nunique():,}"],
        ['Superhosts', f"{master[master['host_is_superhost']==True].shape[0]:,}"],
        ['Neighbourhoods', f"{master['neighbourhood_cleansed'].nunique()}"],
        ['Avg Nightly Price', f"{master['price_clean'].mean():.0f} THB"],
        ['Median Nightly Price', f"{master['price_clean'].median():.0f} THB"],
        ['Avg Occupancy Rate', f"{master['occupancy_rate'].mean():.1f}%"],
        ['Total Reviews', "583,333"],
        ['Positive Sentiment', "81.96%"],
    ]
    kpi_table = Table(kpi_data, colWidths=[3*inch, 3*inch])
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#FF5A5F')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 11),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 10),
        ('ROWBACKGROUNDS', (0,1), (-1,-1),
         [colors.white, colors.HexColor('#FFF5F5')]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    content.append(kpi_table)

    # PRICE ANALYSIS
    content.append(Paragraph("Price Analysis", heading_style))
    content.append(Paragraph("Top 10 Neighbourhoods by Average Price", subheading_style))

    top_price = master.groupby('neighbourhood_cleansed')['price_clean']\
        .mean().nlargest(10).reset_index()
    price_data = [['Rank', 'Neighbourhood', 'Avg Price (THB)']]
    for i, row in top_price.iterrows():
        price_data.append([
            str(top_price.index.get_loc(i) + 1),
            row['neighbourhood_cleansed'],
            f"{row['price_clean']:.0f}"
        ])

    price_table = Table(price_data, colWidths=[1*inch, 3*inch, 2*inch])
    price_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#484848')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('ROWBACKGROUNDS', (0,1), (-1,-1),
         [colors.white, colors.HexColor('#F5F5F5')]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    content.append(price_table)

    # ROOM TYPE ANALYSIS
    content.append(Paragraph("Room Type Analysis", subheading_style))
    room_data_raw = master.groupby('room_type').agg(
        count=('id', 'count'),
        avg_price=('price_clean', 'mean'),
        avg_occupancy=('occupancy_rate', 'mean')
    ).reset_index()

    room_table_data = [['Room Type', 'Listings', 'Avg Price (THB)', 'Avg Occupancy']]
    for _, row in room_data_raw.iterrows():
        room_table_data.append([
            row['room_type'],
            f"{row['count']:,}",
            f"{row['avg_price']:.0f}",
            f"{row['avg_occupancy']:.1f}%"
        ])

    room_table = Table(room_table_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1.5*inch])
    room_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#484848')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('ROWBACKGROUNDS', (0,1), (-1,-1),
         [colors.white, colors.HexColor('#F5F5F5')]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    content.append(room_table)

    # HYPOTHESIS TESTS
    content.append(Paragraph("Statistical Analysis", heading_style))
    content.append(Paragraph("Hypothesis Test Results", subheading_style))
    content.append(Paragraph(
        "Five Mann-Whitney U and Kruskal-Wallis tests were conducted to validate "
        "market assumptions:",
        body_style
    ))

    hyp_data = [
        ['Test', 'Finding', 'P-Value', 'Result'],
        ['Superhost Pricing', 'Superhosts charge significantly\ndifferent prices',
         '0.000044', 'Significant'],
        ['Room Type Occupancy', 'Entire homes have higher\noccupancy than private rooms',
         '<0.001', 'Significant'],
        ['Price-Review Correlation', 'Weak positive correlation\nbetween price and reviews',
         '<0.001', 'Significant'],
        ['Instant Booking', 'Non-instant listings have\nhigher occupancy',
         '0.000031', 'Significant'],
        ['Neighbourhood Pricing', 'Significant price differences\nacross neighbourhoods',
         '<0.001', 'Significant'],
    ]

    hyp_table = Table(hyp_data, colWidths=[1.5*inch, 2.5*inch, 1*inch, 1.2*inch])
    hyp_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#FF5A5F')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('ROWBACKGROUNDS', (0,1), (-1,-1),
         [colors.white, colors.HexColor('#FFF5F5')]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    content.append(hyp_table)

    # SENTIMENT ANALYSIS
    content.append(Paragraph("Sentiment Analysis", heading_style))
    content.append(Paragraph(
        """VADER sentiment analysis was applied to 10,000 guest reviews revealing 
        overwhelmingly positive guest experiences. 81.96% of reviews were classified 
        as positive with an average compound score of 0.6688. A declining sentiment 
        trend from 2011 (0.85) to 2024 (0.52) suggests guests are becoming more 
        critical as the platform matures, a common pattern in maturing markets.""",
        body_style
    ))

    sent_data = [
        ['Sentiment', 'Count', 'Percentage'],
        ['Positive', '8,196', '81.96%'],
        ['Neutral', '1,417', '14.17%'],
        ['Negative', '387', '3.87%'],
    ]
    sent_table = Table(sent_data, colWidths=[2*inch, 2*inch, 2*inch])
    sent_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#484848')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('ROWBACKGROUNDS', (0,1), (-1,-1),
         [colors.white, colors.HexColor('#F5F5F5')]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    content.append(sent_table)

    # PRICE PREDICTION
    content.append(Paragraph("Predictive Modeling", heading_style))
    content.append(Paragraph(
        """A price prediction model was built using three algorithms. 
        Gradient Boosting achieved the best performance with R2=0.51, 
        predicting nightly prices within ±866 THB on average. 
        Key price drivers identified: number of bedrooms (27%), 
        host tenure (22%), and availability (11%).""",
        body_style
    ))

    model_data = [
        ['Model', 'MAE (THB)', 'RMSE (THB)', 'R2 Score'],
        ['Linear Regression', '1,107', '2,415', '0.34'],
        ['Random Forest', '866', '2,113', '0.49'],
        ['Gradient Boosting', '941', '2,070', '0.51'],
    ]
    model_table = Table(model_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1.5*inch])
    model_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#FF5A5F')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('ROWBACKGROUNDS', (0,1), (-1,-1),
         [colors.white, colors.HexColor('#FFF5F5')]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('PADDING', (0,0), (-1,-1), 8),
        ('BACKGROUND', (0,3), (-1,3), colors.HexColor('#FFE5E5')),
    ]))
    content.append(model_table)

    # RECOMMENDATIONS
    content.append(Paragraph("Business Recommendations", heading_style))
    recommendations = [
        ("1. Target Vadhana & Parthum Wan",
         "These neighbourhoods command the highest prices and occupancy rates. "
         "New hosts should consider these areas for maximum revenue potential."),
        ("2. Focus on Entire Home/Apt",
         "Entire homes achieve 25.85% occupancy vs 19.04% for private rooms. "
         "Converting private room listings to entire home rentals could boost revenue."),
        ("3. Build Host Tenure",
         "Host tenure is the 2nd most important price predictor (22%). "
         "Long-term platform presence significantly impacts pricing power."),
        ("4. Reconsider Instant Booking",
         "Contrary to expectations, non-instant bookable listings show higher "
         "occupancy (24.66% vs 22.76%). Hosts should evaluate their booking strategy."),
        ("5. Monitor Sentiment Trends",
         "Declining sentiment scores suggest guests have higher expectations. "
         "Hosts should focus on improving cleanliness and communication scores."),
    ]

    for title, text in recommendations:
        content.append(Paragraph(f"<b>{title}</b>", body_style))
        content.append(Paragraph(text, body_style))
        content.append(Spacer(1, 0.1*inch))

    # FOOTER
    content.append(Spacer(1, 0.3*inch))
    content.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
    content.append(Spacer(1, 0.1*inch))
    content.append(Paragraph(
        f"Report generated automatically on {datetime.now().strftime('%B %d, %Y at %H:%M')} | "
        f"Data: Inside Airbnb Bangkok (Sep 2025) | "
        f"Expernetic Data Engineer Intern Assessment",
        ParagraphStyle('Footer', parent=styles['Normal'],
                      fontSize=8, textColor=colors.grey, alignment=TA_CENTER)
    ))

    # Build PDF
    doc.build(content)
    print(f"Report saved to: {output_path}")
    return output_path

if __name__ == "__main__":
    generate_report()