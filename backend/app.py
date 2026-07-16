"""
Flask API for Brent Oil Change Point Analysis Dashboard
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
from data_loader import (
    get_price_series,
    get_events,
    get_change_points,
    get_statistics,
    load_price_data,
    load_events_data
)

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'message': 'Brent Oil API is running!'})


@app.route('/api/prices', methods=['GET'])
def get_prices():
    """
    Get price data with optional date filtering.
    Query params:
        - start: start date (YYYY-MM-DD)
        - end: end date (YYYY-MM-DD)
    """
    try:
        start = request.args.get('start')
        end = request.args.get('end')
        
        df = load_price_data()
        
        if start:
            df = df[df.index >= pd.to_datetime(start)]
        if end:
            df = df[df.index <= pd.to_datetime(end)]
        
        response = {
            'dates': df.index.strftime('%Y-%m-%d').tolist(),
            'prices': df['Price'].tolist(),
            'ma50': df['MA_50'].tolist() if 'MA_50' in df.columns else [],
            'ma200': df['MA_200'].tolist() if 'MA_200' in df.columns else [],
            'returns': df['Returns'].tolist() if 'Returns' in df.columns else [],
            'volatility': df['Volatility_30d'].tolist() if 'Volatility_30d' in df.columns else []
        }
        
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/events', methods=['GET'])
def get_events_endpoint():
    """Get all events."""
    try:
        return jsonify(get_events())
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/change-points', methods=['GET'])
def get_change_points_endpoint():
    """Get detected change points."""
    try:
        return jsonify(get_change_points())
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/statistics', methods=['GET'])
def get_statistics_endpoint():
    """Get summary statistics."""
    try:
        return jsonify(get_statistics())
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/event-impact', methods=['GET'])
def get_event_impact():
    """
    Get price impact for each event (before vs after 30-day window).
    """
    try:
        df = load_price_data()
        events_df = load_events_data()
        
        impacts = []
        
        for _, event in events_df.iterrows():
            event_date = event['Date']
            
            # 30-day window before and after
            before_start = event_date - pd.Timedelta(days=30)
            after_end = event_date + pd.Timedelta(days=30)
            
            before_prices = df[(df.index >= before_start) & (df.index < event_date)]['Price']
            after_prices = df[(df.index > event_date) & (df.index <= after_end)]['Price']
            
            if len(before_prices) > 0 and len(after_prices) > 0:
                before_avg = float(before_prices.mean())
                after_avg = float(after_prices.mean())
                change_pct = ((after_avg - before_avg) / before_avg) * 100 if before_avg != 0 else 0
                
                impacts.append({
                    'event_id': int(event['Event_ID']),
                    'event_name': event['Event_Name'],
                    'date': event_date.strftime('%Y-%m-%d'),
                    'category': event['Category'],
                    'price_before': round(before_avg, 2),
                    'price_after': round(after_avg, 2),
                    'change_percent': round(change_pct, 2)
                })
        
        return jsonify({'impacts': impacts})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/event-correlation', methods=['GET'])
def get_event_correlation():
    """
    Get all event data with price correlations for the frontend.
    """
    try:
        df = load_price_data()
        events_df = load_events_data()
        
        # Get prices on event dates
        event_data = []
        for _, event in events_df.iterrows():
            event_date = event['Date']
            
            # Find price closest to event date
            if event_date in df.index:
                price = float(df.loc[event_date, 'Price'])
            else:
                idx = df.index.get_indexer([event_date], method='nearest')[0]
                price = float(df.iloc[idx]['Price'])
            
            # Get 30-day price trend around event
            before_date = event_date - pd.Timedelta(days=30)
            after_date = event_date + pd.Timedelta(days=30)
            
            trend_prices = df[(df.index >= before_date) & (df.index <= after_date)]
            
            event_data.append({
                'id': int(event['Event_ID']),
                'name': event['Event_Name'],
                'date': event_date.strftime('%Y-%m-%d'),
                'category': event['Category'],
                'price_at_event': price,
                'trend_dates': trend_prices.index.strftime('%Y-%m-%d').tolist(),
                'trend_prices': trend_prices['Price'].tolist()
            }) 
        
        return jsonify({'correlations': event_data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 