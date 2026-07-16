import React, { useState, useEffect } from 'react';
import PriceChart from './PriceChart';
import EventList from './EventList';
import StatsCards from './StatsCards';
import { fetchPrices, fetchEvents, fetchChangePoints, fetchStatistics, fetchEventImpacts } from '../api';
import './Dashboard.css';

const Dashboard = () => {
    const [prices, setPrices] = useState([]);
    const [events, setEvents] = useState([]);
    const [changePoints, setChangePoints] = useState([]);
    const [statistics, setStatistics] = useState(null);
    const [impacts, setImpacts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [dateRange, setDateRange] = useState({ start: '', end: '' });
    const [selectedEvent, setSelectedEvent] = useState(null);

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        try {
            setLoading(true);
            const [pricesData, eventsData, cpData, statsData, impactsData] = await Promise.all([
                fetchPrices(),
                fetchEvents(),
                fetchChangePoints(),
                fetchStatistics(),
                fetchEventImpacts()
            ]);

            setPrices(pricesData);
            setEvents(eventsData.events || []);
            setChangePoints(cpData.change_points || []);
            setStatistics(statsData);
            setImpacts(impactsData.impacts || []);
            setError(null);
        } catch (err) {
            setError('Failed to load data. Please check if the backend is running.');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const handleDateFilter = async () => {
        try {
            setLoading(true);
            const data = await fetchPrices(dateRange.start, dateRange.end);
            setPrices(data);
        } catch (err) {
            setError('Failed to filter data.');
        } finally {
            setLoading(false);
        }
    };

    const handleEventClick = (event) => {
        setSelectedEvent(event);
    };

    if (loading) {
        return <div className="loading">Loading dashboard...</div>;
    }

    if (error) {
        return <div className="error">{error}</div>;
    }

    return (
        <div className="dashboard">
            <header className="dashboard-header">
                <h1>Brent Oil Price Analysis Dashboard</h1>
                <p>Interactive visualization of geopolitical events and their impact on Brent oil prices</p>
            </header>

            {statistics && <StatsCards stats={statistics} />}

            <div className="filter-section">
                <div className="filter-controls">
                    <label>
                        Start Date:
                        <input
                            type="date"
                            value={dateRange.start}
                            onChange={(e) => setDateRange({ ...dateRange, start: e.target.value })}
                        />
                    </label>
                    <label>
                        End Date:
                        <input
                            type="date"
                            value={dateRange.end}
                            onChange={(e) => setDateRange({ ...dateRange, end: e.target.value })}
                        />
                    </label>
                    <button onClick={handleDateFilter}>Apply Filter</button>
                    <button onClick={() => { setDateRange({ start: '', end: '' }); loadData(); }}>
                        Reset
                    </button>
                </div>
            </div>

            <div className="dashboard-content">
                <div className="chart-section">
                    <PriceChart
                        prices={prices}
                        events={events}
                        changePoints={changePoints}
                        selectedEvent={selectedEvent}
                    />
                </div>
                <div className="sidebar">
                    <div className="events-section">
                        <h3>Key Events</h3>
                        <EventList
                            events={events}
                            impacts={impacts}
                            onEventClick={handleEventClick}
                            selectedEvent={selectedEvent}
                        />
                    </div>
                    <div className="change-points-section">
                        <h3>Detected Change Points</h3>
                        {changePoints.length === 0 ? (
                            <p>No change points detected.</p>
                        ) : (
                            <ul>
                                {changePoints.map((cp, idx) => (
                                    <li key={idx}>
                                        <strong>{cp.date}</strong>
                                        <span>Price: ${cp.price_at_change?.toFixed(2) || 'N/A'}</span>
                                    </li>
                                ))}
                            </ul>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Dashboard; 