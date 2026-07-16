import React from 'react';
import './StatsCards.css';

const StatsCards = ({ stats }) => {
    if (!stats) return null;

    const cards = [
        {
            title: 'Total Observations',
            value: stats.total_observations || 0,
            icon: '📊',
            color: '#1a2a6c'
        },
        {
            title: 'Price Range',
            value: `$${stats.price_stats?.min?.toFixed(2) || 0} - $${stats.price_stats?.max?.toFixed(2) || 0}`,
            icon: '💰',
            color: '#2e7d32'
        },
        {
            title: 'Average Price',
            value: `$${stats.price_stats?.mean?.toFixed(2) || 0}`,
            icon: '📈',
            color: '#fdbb2d'
        },
        {
            title: 'Avg Volatility',
            value: `${(stats.volatility_stats?.mean || 0).toFixed(2)}%`,
            icon: '📉',
            color: '#b21f1f'
        },
        {
            title: 'Date Range',
            value: `${stats.date_range?.start || 'N/A'} to ${stats.date_range?.end || 'N/A'}`,
            icon: '📅',
            color: '#1976d2'
        }
    ];

    return (
        <div className="stats-cards">
            {cards.map((card, idx) => (
                <div key={idx} className="stat-card" style={{ borderTop: `4px solid ${card.color}` }}>
                    <div className="stat-icon">{card.icon}</div>
                    <div className="stat-title">{card.title}</div>
                    <div className="stat-value">{card.value}</div>
                </div>
            ))}
        </div>
    );
};

export default StatsCards; 