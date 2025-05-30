"""
api.py - API routes for Stock Oracle MVP

This module contains all the API routes for the Stock Oracle MVP, providing
data for the dashboard visualizations and stock information.
"""

import random
import datetime
import json
import yfinance as yf
import pandas as pd
import numpy as np
from flask import Blueprint, jsonify

# Create blueprint for API routes
api_bp = Blueprint('api', __name__)

# Sample data for testing
AI_COMPANIES = ['NVDA', 'AMD', 'INTC', 'MSFT', 'GOOGL', 'AAPL']
POWER_COMPANIES = ['NEE', 'DUK', 'SO', 'AEP', 'XEL', 'D']
WATER_COMPANIES = ['AWK', 'WTR', 'CWT', 'YORW', 'MSEX', 'AWR']
PICKS_COMPANIES = ['ANET', 'CDNS', 'SNPS', 'AVGO', 'LRCX', 'KLAC', 'ASML', 'TSM']

# Cache for stock data to avoid repeated API calls
STOCK_CACHE = {}
CACHE_EXPIRY = 3600  # 1 hour in seconds

@api_bp.route('/top-picks', methods=['GET'])
def get_top_picks():
    """Return top stock picks based on correlation analysis."""
    picks = []
    
    # Generate sample data for demonstration
    for symbol in random.sample(PICKS_COMPANIES, 6):
        stock_data = get_stock_data(symbol)
        
        if stock_data:
            picks.append({
                'symbol': symbol,
                'name': stock_data['name'],
                'price': stock_data['price'],
                'change_percent': stock_data['change_percent'],
                'correlation_score': random.uniform(0.65, 0.95)
            })
    
    # Sort by correlation score
    picks = sorted(picks, key=lambda x: x['correlation_score'], reverse=True)
    
    return jsonify({'picks': picks})

@api_bp.route('/correlation-visualization', methods=['GET'])
def get_correlation_visualization():
    """Return data for the multi-dimensional correlation visualization."""
    # Create sample nodes for visualization
    nodes = []
    edges = []
    
    # Add AI companies
    for symbol in AI_COMPANIES[:3]:
        nodes.append({
            'id': symbol,
            'name': get_stock_name(symbol),
            'group': 'ai',
            'size': 15
        })
    
    # Add power infrastructure companies
    for symbol in POWER_COMPANIES[:2]:
        nodes.append({
            'id': symbol,
            'name': get_stock_name(symbol),
            'group': 'power',
            'size': 12
        })
    
    # Add water infrastructure companies
    for symbol in WATER_COMPANIES[:2]:
        nodes.append({
            'id': symbol,
            'name': get_stock_name(symbol),
            'group': 'water',
            'size': 12
        })
    
    # Add picks & shovels companies
    for symbol in PICKS_COMPANIES[:5]:
        nodes.append({
            'id': symbol,
            'name': get_stock_name(symbol),
            'group': 'picks',
            'size': 10
        })
    
    # Create edges between nodes
    for i, node in enumerate(nodes):
        # Connect AI companies to infrastructure
        if node['group'] == 'ai':
            for other in nodes:
                if other['group'] in ['power', 'water']:
                    edges.append({
                        'source': node['id'],
                        'target': other['id'],
                        'weight': random.uniform(0.5, 0.9)
                    })
        
        # Connect picks & shovels to AI companies
        if node['group'] == 'picks':
            for other in nodes:
                if other['group'] == 'ai' and random.random() > 0.3:
                    edges.append({
                        'source': node['id'],
                        'target': other['id'],
                        'weight': random.uniform(0.6, 0.95)
                    })
    
    return jsonify({
        'nodes': nodes,
        'edges': edges
    })

@api_bp.route('/growth-patterns', methods=['GET'])
def get_growth_patterns():
    """Return data for the growth pattern matcher visualization."""
    # Generate sample data for the past 12 months
    months = [(datetime.datetime.now() - datetime.timedelta(days=30*i)).strftime('%b %Y') for i in range(12)]
    months.reverse()
    
    # Generate growth patterns for infrastructure
    ai_growth = generate_growth_pattern(base=100, volatility=0.15, trend=0.08)
    power_growth = generate_growth_pattern(base=100, volatility=0.08, trend=0.04, correlation_with=ai_growth, correlation_strength=0.7, lag=2)
    water_growth = generate_growth_pattern(base=100, volatility=0.06, trend=0.03, correlation_with=ai_growth, correlation_strength=0.6, lag=3)
    
    # Generate company growth patterns
    companies = {}
    for symbol in random.sample(PICKS_COMPANIES, 3):
        # Generate growth pattern with some correlation to infrastructure
        growth = generate_growth_pattern(
            base=100, 
            volatility=0.12, 
            trend=0.05, 
            correlation_with=ai_growth, 
            correlation_strength=random.uniform(0.5, 0.9),
            lag=random.randint(0, 2)
        )
        
        companies[symbol] = {
            'name': get_stock_name(symbol),
            'growth': growth
        }
    
    return jsonify({
        'months': months,
        'infrastructure': {
            'ai': ai_growth,
            'power': power_growth,
            'water': water_growth
        },
        'companies': companies
    })

@api_bp.route('/supply-chain-map', methods=['GET'])
def get_supply_chain_map():
    """Return data for the supply chain relationship map."""
    nodes = []
    edges = []
    
    # Add AI companies as root nodes
    for symbol in AI_COMPANIES[:2]:
        nodes.append({
            'id': symbol,
            'name': get_stock_name(symbol),
            'type': 'ai'
        })
    
    # Add tier 1 suppliers (picks & shovels)
    tier1_suppliers = {}
    for ai_symbol in AI_COMPANIES[:2]:
        # Each AI company has 2-3 tier 1 suppliers
        suppliers = random.sample(PICKS_COMPANIES, random.randint(2, 3))
        tier1_suppliers[ai_symbol] = suppliers
        
        for supplier in suppliers:
            if supplier not in [node['id'] for node in nodes]:
                nodes.append({
                    'id': supplier,
                    'name': get_stock_name(supplier),
                    'type': 'tier1'
                })
            
            edges.append({
                'source': supplier,
                'target': ai_symbol
            })
    
    # Add tier 2 suppliers
    for ai_symbol, suppliers in tier1_suppliers.items():
        for supplier in suppliers:
            # Each tier 1 supplier has 1-2 tier 2 suppliers
            tier2_count = random.randint(1, 2)
            tier2_symbols = []
            
            # Create unique tier 2 supplier IDs
            for i in range(tier2_count):
                tier2_symbol = f"T2-{supplier}-{i+1}"
                tier2_symbols.append(tier2_symbol)
                
                nodes.append({
                    'id': tier2_symbol,
                    'name': f"Supplier {tier2_symbol}",
                    'type': 'tier2'
                })
                
                edges.append({
                    'source': tier2_symbol,
                    'target': supplier
                })
    
    return jsonify({
        'nodes': nodes,
        'edges': edges
    })

@api_bp.route('/news-feed', methods=['GET'])
def get_news_feed():
    """Return data for the news and signals feed."""
    news_items = []
    
    # Sample news headlines
    headlines = [
        "AI Data Center Expansion Accelerates, Power Demands Surge",
        "Water Cooling Solutions See Record Demand from Tech Sector",
        "Chip Supplier Reports Record Backlog for AI Components",
        "Power Grid Upgrades Planned Near Major Data Center Hubs",
        "New AI Chip Design Requires Advanced Cooling Systems",
        "Supply Chain Bottlenecks Emerge for Key AI Components",
        "Infrastructure Spending for AI Deployments Hits New Record",
        "Analysts Highlight Hidden Winners in AI Supply Chain",
        "Water Usage in Data Centers Becomes Environmental Focus",
        "Power Companies Announce New Partnerships with Tech Giants"
    ]
    
    # Generate sample news items
    for i in range(8):
        # Select random headline
        headline = random.choice(headlines)
        headlines.remove(headline)  # Remove to avoid duplicates
        
        # Generate random time in the past 24 hours
        hours_ago = random.randint(0, 23)
        minutes_ago = random.randint(0, 59)
        
        if hours_ago == 0:
            time_str = f"{minutes_ago}m ago"
        else:
            time_str = f"{hours_ago}h ago"
        
        # Determine sentiment
        sentiments = ['positive', 'neutral', 'negative']
        sentiment_weights = [0.5, 0.3, 0.2]
        sentiment = random.choices(sentiments, weights=sentiment_weights)[0]
        
        # Generate tags
        all_tags = ['AI', 'Power', 'Water', 'Supply Chain', 'Infrastructure', 'Chips', 'Cooling', 'Data Centers']
        tags = random.sample(all_tags, random.randint(1, 3))
        
        news_items.append({
            'title': headline,
            'source': random.choice(['Market Watch', 'Bloomberg', 'Reuters', 'CNBC', 'WSJ']),
            'time': time_str,
            'sentiment': sentiment,
            'tags': tags
        })
    
    return jsonify({'news': news_items})

@api_bp.route('/stock/<symbol>', methods=['GET'])
def get_stock_details(symbol):
    """Return detailed information about a specific stock."""
    stock_data = get_stock_data(symbol)
    
    if not stock_data:
        return jsonify({'error': 'Stock data not available'}), 404
    
    # Generate correlation data
    months = [(datetime.datetime.now() - datetime.timedelta(days=30*i)).strftime('%b %Y') for i in range(12)]
    months.reverse()
    
    company_growth = generate_growth_pattern(base=100, volatility=0.12, trend=0.05)
    ai_growth = generate_growth_pattern(base=100, volatility=0.15, trend=0.08, correlation_with=company_growth, correlation_strength=0.7)
    power_growth = generate_growth_pattern(base=100, volatility=0.08, trend=0.04, correlation_with=company_growth, correlation_strength=0.6)
    water_growth = generate_growth_pattern(base=100, volatility=0.06, trend=0.03, correlation_with=company_growth, correlation_strength=0.5)
    
    # Calculate correlation coefficients
    ai_corr = calculate_correlation(company_growth, ai_growth)
    power_corr = calculate_correlation(company_growth, power_growth)
    water_corr = calculate_correlation(company_growth, water_growth)
    
    # Generate news items specific to this stock
    news_items = generate_stock_news(symbol)
    
    return jsonify({
        'symbol': symbol,
        'name': stock_data['name'],
        'price': stock_data['price'],
        'change_percent': stock_data['change_percent'],
        'market_cap': stock_data['market_cap'],
        'volume': stock_data['volume'],
        'fifty_two_week_range': stock_data['fifty_two_week_range'],
        'correlation_data': {
            'months': months,
            'company_growth': company_growth,
            'ai_growth': ai_growth,
            'power_growth': power_growth,
            'water_growth': water_growth,
            'correlations': {
                'ai': round(ai_corr, 2),
                'power': round(power_corr, 2),
                'water': round(water_corr, 2)
            }
        },
        'news': news_items
    })

# Helper functions
def get_stock_data(symbol):
    """Get stock data from cache or API."""
    now = datetime.datetime.now().timestamp()
    
    # Check cache first
    if symbol in STOCK_CACHE and now - STOCK_CACHE[symbol]['timestamp'] < CACHE_EXPIRY:
        return STOCK_CACHE[symbol]['data']
    
    try:
        # Try to get real data from yfinance
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        # Extract relevant information
        stock_data = {
            'name': info.get('shortName', info.get('longName', symbol)),
            'price': info.get('currentPrice', info.get('previousClose', 100)),
            'change_percent': info.get('regularMarketChangePercent', random.uniform(-5, 5)),
            'market_cap': info.get('marketCap', random.randint(1000000000, 100000000000)),
            'volume': info.get('volume', random.randint(1000000, 10000000)),
            'fifty_two_week_range': f"{info.get('fiftyTwoWeekLow', 0):.2f} - {info.get('fiftyTwoWeekHigh', 0):.2f}"
        }
        
        # Cache the data
        STOCK_CACHE[symbol] = {
            'data': stock_data,
            'timestamp': now
        }
        
        return stock_data
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        
        # Generate fallback data
        fallback_data = {
            'name': get_stock_name(symbol),
            'price': random.uniform(50, 500),
            'change_percent': random.uniform(-5, 5),
            'market_cap': random.randint(1000000000, 100000000000),
            'volume': random.randint(1000000, 10000000),
            'fifty_two_week_range': f"{random.uniform(30, 100):.2f} - {random.uniform(100, 600):.2f}"
        }
        
        # Cache the fallback data
        STOCK_CACHE[symbol] = {
            'data': fallback_data,
            'timestamp': now
        }
        
        return fallback_data

def get_stock_name(symbol):
    """Get stock name from cache or generate a placeholder."""
    if symbol in STOCK_CACHE and 'data' in STOCK_CACHE[symbol]:
        return STOCK_CACHE[symbol]['data']['name']
    
    # Company name mapping for demo
    name_map = {
        'NVDA': 'NVIDIA Corporation',
        'AMD': 'Advanced Micro Devices, Inc.',
        'INTC': 'Intel Corporation',
        'MSFT': 'Microsoft Corporation',
        'GOOGL': 'Alphabet Inc.',
        'AAPL': 'Apple Inc.',
        'NEE': 'NextEra Energy, Inc.',
        'DUK': 'Duke Energy Corporation',
        'SO': 'Southern Company',
        'AEP': 'American Electric Power',
        'XEL': 'Xcel Energy Inc.',
        'D': 'Dominion Energy, Inc.',
        'AWK': 'American Water Works',
        'WTR': 'Essential Utilities, Inc.',
        'CWT': 'California Water Service',
        'YORW': 'York Water Company',
        'MSEX': 'Middlesex Water Company',
        'AWR': 'American States Water',
        'ANET': 'Arista Networks, Inc.',
        'CDNS': 'Cadence Design Systems',
        'SNPS': 'Synopsys, Inc.',
        'AVGO': 'Broadcom Inc.',
        'LRCX': 'Lam Research Corporation',
        'KLAC': 'KLA Corporation',
        'ASML': 'ASML Holding N.V.',
        'TSM': 'Taiwan Semiconductor'
    }
    
    return name_map.get(symbol, f"{symbol} Inc.")

def generate_growth_pattern(base=100, volatility=0.1, trend=0.05, correlation_with=None, correlation_strength=0, lag=0):
    """Generate a growth pattern with optional correlation to another pattern."""
    length = 12  # 12 months
    
    if correlation_with is not None and correlation_strength > 0:
        # Create a pattern correlated with the provided one
        independent_component = np.random.normal(0, volatility, length)
        
        # Apply lag if specified
        if lag > 0 and lag < length:
            correlated_base = np.pad(correlation_with, (lag, 0), 'edge')[:-lag]
        else:
            correlated_base = correlation_with
            
        # Mix independent and correlated components
        changes = (1 - correlation_strength) * independent_component + correlation_strength * (np.diff(np.pad(correlated_base, (1, 0), 'edge')) / np.pad(correlated_base, (1, 0), 'edge')[:-1])
    else:
        # Create an independent pattern
        changes = np.random.normal(0, volatility, length)
    
    # Add trend
    changes = changes + trend
    
    # Convert to cumulative growth
    pattern = [base]
    for change in changes:
        pattern.append(pattern[-1] * (1 + change))
    
    # Normalize to start at base
    pattern = [p * base / pattern[0] for p in pattern]
    
    # Round to 2 decimal places
    pattern = [round(p, 2) for p in pattern]
    
    return pattern[1:]  # Remove the initial base value

def calculate_correlation(series1, series2):
    """Calculate correlation coefficient between two series."""
    return np.corrcoef(series1, series2)[0, 1]

def generate_stock_news(symbol):
    """Generate news items specific to a stock."""
    news_items = []
    
    # Templates for news headlines
    templates = [
        "{symbol} Reports Strong Quarterly Results, Exceeding Expectations",
        "{symbol} Announces New Partnership with Leading AI Company",
        "Analysts Upgrade {symbol} on Strong Growth Prospects",
        "{symbol} Expands Manufacturing Capacity for AI Components",
        "Supply Chain Constraints Could Impact {symbol}'s Production",
        "{symbol} Introduces New Technology for Data Center Efficiency",
        "Institutional Investors Increase Stakes in {symbol}",
        "{symbol} CEO Discusses Future Growth Strategy in Interview"
    ]
    
    # Generate 5 news items
    for i in range(5):
        # Select random template
        template = random.choice(templates)
        templates.remove(template)  # Remove to avoid duplicates
        
        # Generate random date in the past month
        days_ago = random.randint(0, 30)
        news_date = (datetime.datetime.now() - datetime.timedelta(days=days_ago)).strftime('%b %d')
        
        # Determine sentiment
        sentiments = ['positive', 'neutral', 'negative']
        sentiment_weights = [0.6, 0.3, 0.1]
        sentiment = random.choices(sentiments, weights=sentiment_weights)[0]
        
        news_items.append({
            'title': template.format(symbol=symbol),
            'date': news_date,
            'sentiment': sentiment
        })
    
    # Sort by date (most recent first)
    news_items = sorted(news_items, key=lambda x: datetime.datetime.strptime(x['date'], '%b %d'), reverse=True)
    
    return news_items
