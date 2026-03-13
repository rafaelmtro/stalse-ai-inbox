'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { Ticket } from '@/types';
import { fetchTickets } from '@/lib/api';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  Cell
} from 'recharts';

export default function DashboardPage() {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setIsLoading(true);
      const data = await fetchTickets();
      setTickets(data);
    } catch (err) {
      setError('Failed to load dashboard data.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  // Process data for charts
  const categoriesMap = tickets.reduce((acc: Record<string, number>, t) => {
    acc[t.category] = (acc[t.category] || 0) + 1;
    return acc;
  }, {});

  const chartData = Object.keys(categoriesMap).map(cat => ({
    name: cat,
    count: categoriesMap[cat]
  })).sort((a, b) => b.count - a.count);

  const metrics = {
    total: tickets.length,
    pending: tickets.filter(t => t.status === 'pending').length,
    resolved: tickets.filter(t => t.status === 'resolved').length,
    highPriority: tickets.filter(t => t.priority === 'high').length,
  };

  return (
    <div className="min-h-screen bg-brand-black p-4 md:p-8">
      <div className="max-w-6xl mx-auto">
        <header className="mb-10 flex flex-col md:flex-row md:items-center justify-between gap-6 pb-6 border-b border-brand-gray">
          <div>
            <h1 className="text-3xl font-bold text-brand-text flex items-center gap-2">
              <span className="text-brand-orange">AI</span> Analytics
            </h1>
            <p className="text-brand-text-muted mt-2 text-sm">Real-time metrics and ticket distribution.</p>
          </div>
          
          <Link 
            href="/tickets"
            className="bg-brand-orange hover:bg-brand-orange-hover px-8 py-2 rounded font-medium text-white transition-all shadow-lg hover:shadow-brand-orange/20"
          >
            TICKETS
          </Link>
        </header>

        {error && (
          <div className="p-4 bg-red-900/50 border border-red-500 rounded text-red-200 mb-8 text-center">
            {error}
          </div>
        )}

        {isLoading ? (
          <div className="text-center py-20 text-brand-text-muted">Loading metrics...</div>
        ) : (
          <div className="space-y-8">
            {/* Metrics Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              {[
                { label: 'Total Tickets', value: metrics.total, color: 'text-brand-text' },
                { label: 'Pending', value: metrics.pending, color: 'text-brand-orange' },
                { label: 'Resolved', value: metrics.resolved, color: 'text-green-500' },
                { label: 'High Priority', value: metrics.highPriority, color: 'text-red-500' },
              ].map((m, i) => (
                <div key={i} className="card-b2b p-6 rounded-lg">
                  <p className="text-xs font-bold uppercase tracking-wider text-brand-text-muted mb-2">{m.label}</p>
                  <p className={`text-3xl font-bold ${m.color}`}>{m.value}</p>
                </div>
              ))}
            </div>

            {/* Chart Section */}
            <div className="card-b2b p-8 rounded-lg">
              <h2 className="text-xl font-bold mb-8 text-brand-text">Tickets by Category</h2>
              <div className="h-[400px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={chartData} layout="vertical" margin={{ left: 40, right: 40 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#2A2A2A" horizontal={false} />
                    <XAxis type="number" hide />
                    <YAxis 
                      dataKey="name" 
                      type="category" 
                      stroke="#A0A0A0" 
                      fontSize={12}
                      width={120}
                    />
                    <Tooltip 
                      cursor={{ fill: 'rgba(255, 102, 0, 0.05)' }}
                      contentStyle={{ 
                        backgroundColor: '#1A1A1A', 
                        border: '1px solid #2A2A2A',
                        borderRadius: '4px',
                        color: '#EAEAEA'
                      }}
                    />
                    <Bar dataKey="count" radius={[0, 4, 4, 0]} barSize={24}>
                      {chartData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill="#FF6600" />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
