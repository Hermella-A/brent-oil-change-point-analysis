import React from 'react';
import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
    ReferenceLine,
    ResponsiveContainer,
    Brush,
    Scatter,
    ComposedChart
} from 'recharts';

const PriceChart = ({ prices, events, changePoints, selectedEvent }) => {
    if (!prices || !prices.dates || prices.dates.length === 0) {
        return <div>No price data available.</div>;
    }

    // Prepare data for Recharts
    const chartData = prices.dates.map((date, i) => ({
        date: date,
        price: prices.prices[i] || 0,
        ma50: prices.ma50 && prices.ma50[i] ? prices.ma50[i] : null,
        ma200: prices.ma200 && prices.ma200[i] ? prices.ma200[i] : null,
        volatility: prices.volatility && prices.volatility[i] ? prices.volatility[i] : null,
        returns: prices.returns && prices.returns[i] ? prices.returns[i] : null,
    }));

    // Add events as reference lines
    const eventLines = events.map(event => ({
        date: event.Date,
        name: event.Event_Name,
        category: event.Category
    }));

    // Add change points
    const changePointLines = changePoints.map(cp => ({
        date: cp.date,
        name: 'Change Point'
    }));

    // Find the closest data point for an event
    const findClosestPrice = (eventDate) => {
        const idx = chartData.findIndex(d => d.date === eventDate);
        if (idx >= 0) return chartData[idx];
        // Find nearest
        let nearest = chartData[0];
        let minDiff = Infinity;
        chartData.forEach(d => {
            const diff = Math.abs(new Date(d.date) - new Date(eventDate));
            if (diff < minDiff) {
                minDiff = diff;
                nearest = d;
            }
        });
        return nearest;
    };

    // Custom tooltip
    const CustomTooltip = ({ active, payload, label }) => {
        if (!active || !payload) return null;
        
        const eventInfo = events.find(e => e.Date === label);
        
        return (
            <div style={{ background: 'white', padding: '10px', border: '1px solid #ccc', borderRadius: '5px' }}>
                <p><strong>{label}</strong></p>
                {payload.map((p, idx) => (
                    <p key={idx} style={{ color: p.color }}>
                        {p.name}: {typeof p.value === 'number' ? p.value.toFixed(2) : p.value}
                    </p>
                ))}
                {eventInfo && (
                    <div style={{ marginTop: '5px', borderTop: '1px solid #eee', paddingTop: '5px' }}>
                        <p><strong>Event:</strong> {eventInfo.Event_Name}</p>
                        <p><strong>Category:</strong> {eventInfo.Category}</p>
                    </div>
                )}
            </div>
        );
    };

    return (
        <div style={{ width: '100%', height: 500 }}>
            <ResponsiveContainer>
                <ComposedChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" opacity={0.3} />
                    <XAxis 
                        dataKey="date" 
                        tick={{ fontSize: 10 }}
                        interval="preserveStartEnd"
                        minTickGap={30}
                    />
                    <YAxis 
                        yAxisId="left"
                        domain={['auto', 'auto']}
                        label={{ value: 'Price (USD/barrel)', angle: -90, position: 'insideLeft' }}
                    />
                    <YAxis 
                        yAxisId="right"
                        orientation="right"
                        domain={[0, 'auto']}
                        label={{ value: 'Volatility', angle: 90, position: 'insideRight' }}
                    />
                    <Tooltip content={<CustomTooltip />} />
                    <Legend />
                    
                    {/* Price Line */}
                    <Line
                        yAxisId="left"
                        type="monotone"
                        dataKey="price"
                        stroke="#1a2a6c"
                        strokeWidth={1.5}
                        dot={false}
                        name="Brent Price"
                    />
                    
                    {/* 50-day MA */}
                    <Line
                        yAxisId="left"
                        type="monotone"
                        dataKey="ma50"
                        stroke="#fdbb2d"
                        strokeWidth={1}
                        dot={false}
                        name="50-day MA"
                        strokeDasharray="5 5"
                    />
                    
                    {/* 200-day MA */}
                    <Line
                        yAxisId="left"
                        type="monotone"
                        dataKey="ma200"
                        stroke="#b21f1f"
                        strokeWidth={1}
                        dot={false}
                        name="200-day MA"
                        strokeDasharray="5 5"
                    />
                    
                    {/* Volatility */}
                    <Line
                        yAxisId="right"
                        type="monotone"
                        dataKey="volatility"
                        stroke="#2e7d32"
                        strokeWidth={0.8}
                        dot={false}
                        name="Volatility (30d)"
                        opacity={0.6}
                    />

                    {/* Event Reference Lines */}
                    {eventLines.map((event, idx) => {
                        const dataPoint = findClosestPrice(event.date);
                        return (
                            <ReferenceLine
                                key={`event-${idx}`}
                                yAxisId="left"
                                x={event.date}
                                stroke="#b21f1f"
                                strokeDasharray="3 3"
                                strokeWidth={1.5}
                                label={{
                                    value: '🔴',
                                    position: 'top',
                                    fill: '#b21f1f',
                                    fontSize: 14
                                }}
                            />
                        );
                    })}

                    {/* Change Point Reference Lines */}
                    {changePointLines.map((cp, idx) => (
                        <ReferenceLine
                            key={`cp-${idx}`}
                            yAxisId="left"
                            x={cp.date}
                            stroke="#b21f1f"
                            strokeDasharray="8 4"
                            strokeWidth={2}
                            label={{
                                value: '⚡ Change Point',
                                position: 'top',
                                fill: '#b21f1f',
                                fontSize: 12,
                                fontWeight: 'bold'
                            }}
                        />
                    ))}

                    {/* Brush for zooming */}
                    <Brush dataKey="date" height={20} y={470} />
                </ComposedChart>
            </ResponsiveContainer>
        </div>
    );
};

export default PriceChart; 