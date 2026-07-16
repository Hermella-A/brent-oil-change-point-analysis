import React from 'react';

const EventList = ({ events, impacts, onEventClick, selectedEvent }) => {
    if (!events || events.length === 0) {
        return <p>No events loaded.</p>;
    }

    // Sort events by date
    const sortedEvents = [...events].sort((a, b) => new Date(a.Date) - new Date(b.Date));

    // Find impact for an event
    const getImpact = (eventId) => {
        const impact = impacts.find(i => i.event_id === eventId);
        if (impact) {
            return impact.change_percent;
        }
        return null;
    };

    // Format impact display
    const formatImpact = (change) => {
        if (change === null) return 'N/A';
        const sign = change > 0 ? '+' : '';
        return `${sign}${change}%`;
    };

    // Get color for impact
    const getImpactColor = (change) => {
        if (change === null) return '#666';
        if (change > 5) return '#2e7d32';
        if (change > 0) return '#4caf50';
        if (change > -5) return '#ff9800';
        return '#b21f1f';
    };

    // Get color for category
    const getCategoryColor = (category) => {
        const colors = {
            'OPEC Policy': '#1976d2',
            'Geopolitical': '#b21f1f',
            'Geopolitical/Conflict': '#d32f2f',
            'Supply/Demand': '#2e7d32',
            'Geopolitical/Sanctions': '#9c27b0'
        };
        return colors[category] || '#666';
    };

    return (
        <div className="event-list">
            {sortedEvents.map((event) => {
                const impact = getImpact(event.Event_ID);
                const isSelected = selectedEvent && selectedEvent.Event_ID === event.Event_ID;
                
                return (
                    <div
                        key={event.Event_ID}
                        className={`event-item ${isSelected ? 'selected' : ''}`}
                        onClick={() => onEventClick(event)}
                        style={{
                            padding: '10px',
                            marginBottom: '8px',
                            borderLeft: `4px solid ${getCategoryColor(event.Category)}`,
                            background: isSelected ? '#e3f2fd' : 'white',
                            borderRadius: '4px',
                            cursor: 'pointer',
                            boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
                            transition: 'all 0.2s'
                        }}
                    >
                        <div className="event-date" style={{ fontSize: '0.8rem', color: '#666' }}>
                            {event.Date}
                        </div>
                        <div className="event-name" style={{ fontWeight: 'bold', fontSize: '0.9rem' }}>
                            {event.Event_Name}
                        </div>
                        <div className="event-meta" style={{ display: 'flex', gap: '10px', marginTop: '4px' }}>
                            <span className="event-category" style={{
                                fontSize: '0.7rem',
                                padding: '2px 8px',
                                borderRadius: '10px',
                                background: getCategoryColor(event.Category),
                                color: 'white'
                            }}>
                                {event.Category}
                            </span>
                            <span className="event-impact" style={{
                                fontSize: '0.8rem',
                                color: getImpactColor(impact),
                                fontWeight: 'bold'
                            }}>
                                {impact !== null ? `Impact: ${formatImpact(impact)}` : 'No impact data'}
                            </span>
                        </div>
                    </div>
                );
            })}
        </div>
    );
};

export default EventList; 