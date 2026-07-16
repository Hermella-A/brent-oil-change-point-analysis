// API configuration
import axios from 'axios';

const API_BASE = 'http://localhost:5000/api';

export const api = axios.create({
    baseURL: API_BASE,
    timeout: 10000,
});

export const fetchPrices = async (start, end) => {
    const params = {};
    if (start) params.start = start;
    if (end) params.end = end;
    const response = await api.get('/prices', { params });
    return response.data;
};

export const fetchEvents = async () => {
    const response = await api.get('/events');
    return response.data;
};

export const fetchChangePoints = async () => {
    const response = await api.get('/change-points');
    return response.data;
};

export const fetchStatistics = async () => {
    const response = await api.get('/statistics');
    return response.data;
};

export const fetchEventImpacts = async () => {
    const response = await api.get('/event-impact');
    return response.data;
};

export const fetchEventCorrelations = async () => {
    const response = await api.get('/event-correlation');
    return response.data;
}; 