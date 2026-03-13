'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { Ticket, CreateTicketData } from '@/types';
import { fetchTickets, createTicket, updateTicket } from '@/lib/api';
import TicketItem from '@/components/TicketItem';
import TicketForm from '@/components/TicketForm';
import TicketDetails from '@/components/TicketDetails';

export default function TicketsPage() {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [statusFilter, setStatusFilter] = useState<'all' | 'pending' | 'resolved'>('all');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedTicket, setSelectedTicket] = useState<Ticket | null>(null);

  useEffect(() => {
    loadTickets();
  }, []);

  const loadTickets = async () => {
    try {
      setIsLoading(true);
      const data = await fetchTickets();
      // Sort by priority (high first) and then by created_at (newest first)
      const sorted = data.sort((a, b) => {
        if (a.priority === 'high' && b.priority === 'low') return -1;
        if (a.priority === 'low' && b.priority === 'high') return 1;
        return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
      });
      setTickets(sorted);
      setError(null);
    } catch (err) {
      setError('Failed to load tickets. Please try again later.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCreateTicket = async (data: CreateTicketData) => {
    try {
      const newTicket = await createTicket(data);
      setTickets((prev) => [newTicket, ...prev]);
    } catch (err) {
      console.error('Failed to create ticket', err);
      alert('Failed to create ticket. Please try again.');
    }
  };

  const handleUpdateStatus = async (id: number, status: 'pending' | 'resolved') => {
    try {
      setTickets((prev) => 
        prev.map(t => t.id === id ? { ...t, status } : t)
      );
      if (selectedTicket?.id === id) {
        setSelectedTicket({ ...selectedTicket, status });
      }
      await updateTicket(id, { status });
    } catch (err) {
      console.error('Failed to update status', err);
      loadTickets();
    }
  };

  const handleUpdatePriority = async (id: number, priority: 'low' | 'high') => {
    try {
      setTickets((prev) => 
        prev.map(t => t.id === id ? { ...t, priority } : t)
      );
      if (selectedTicket?.id === id) {
        setSelectedTicket({ ...selectedTicket, priority });
      }
      await updateTicket(id, { priority });
    } catch (err) {
      console.error('Failed to update priority', err);
      loadTickets();
    }
  };

  const filteredTickets = tickets.filter(t => 
    statusFilter === 'all' ? true : t.status === statusFilter
  );

  return (
    <div className="min-h-screen bg-brand-black p-4 md:p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header Section */}
        <header className="mb-10 flex flex-col md:flex-row md:items-center justify-between gap-6 pb-6 border-b border-brand-gray">
          <div>
            <h1 className="text-3xl font-bold text-brand-text flex items-center gap-2">
              <span className="text-brand-orange">AI</span> Inbox
            </h1>
            <p className="text-brand-text-muted mt-2 text-sm">Manage support tickets with AI intelligence.</p>
          </div>
          
          <div className="flex flex-wrap items-center gap-4">
            <Link 
              href="/dashboard"
              className="bg-brand-gray hover:bg-brand-gray-light border border-brand-gray-light px-6 py-2 rounded font-medium text-brand-text transition-all text-sm"
            >
              ANALYTICS
            </Link>

            <div className="flex items-center gap-2 border-l border-brand-gray pl-4">
              <label className="text-xs font-medium text-brand-text-muted">FILTER BY STATUS:</label>
              <select 
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value as any)}
                className="bg-brand-gray border border-brand-gray-light text-brand-text text-xs rounded p-2 focus:outline-none focus:border-brand-orange cursor-pointer"
              >
                <option value="all">All Status</option>
                <option value="pending">Pending</option>
                <option value="resolved">Resolved</option>
              </select>
            </div>
            
            <button 
              onClick={() => setIsModalOpen(true)}
              className="btn-primary px-6 py-2 rounded font-medium transition-all shadow-lg hover:shadow-brand-orange/20"
            >
              + New Ticket
            </button>
          </div>
        </header>

        {/* Modal: Create Ticket */}
        {isModalOpen && (
          <TicketForm 
            onSubmit={handleCreateTicket} 
            onClose={() => setIsModalOpen(false)} 
          />
        )}

        {/* Modal: Ticket Details */}
        {selectedTicket && (
          <TicketDetails 
            ticket={selectedTicket} 
            onClose={() => setSelectedTicket(null)} 
          />
        )}

        {/* Error State */}
        {error && (
          <div className="p-4 bg-red-900/50 border border-red-500 rounded text-red-200 mb-8">
            {error}
          </div>
        )}

        {/* Main Content (Table) */}
        <div className="card-b2b rounded-lg overflow-hidden">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-brand-gray/50 text-xs font-bold uppercase tracking-wider text-brand-text-muted border-b border-brand-gray">
                <th className="py-4 px-4 w-32">Created At</th>
                <th className="py-4 px-2 w-48">Customer</th>
                <th className="py-4 px-2">Message</th>
                <th className="py-4 px-2 w-40">Category</th>
                <th className="py-4 px-2 w-32">Priority</th>
                <th className="py-4 px-2 w-32 text-right">Status</th>
              </tr>
            </thead>
            <tbody>
              {isLoading ? (
                <tr>
                  <td colSpan={6} className="py-12 text-center text-brand-text-muted">
                    Loading inbox...
                  </td>
                </tr>
              ) : filteredTickets.length === 0 ? (
                <tr>
                  <td colSpan={6} className="py-12 text-center text-brand-text-muted italic">
                    {statusFilter !== 'all' ? `No ${statusFilter} tickets found.` : "Inbox is empty."}
                  </td>
                </tr>
              ) : (
                filteredTickets.map((ticket) => (
                  <TicketItem
                    key={ticket.id}
                    ticket={ticket}
                    onUpdateStatus={handleUpdateStatus}
                    onUpdatePriority={handleUpdatePriority}
                    onClick={setSelectedTicket}
                  />
                ))
              )}
            </tbody>
          </table>
        </div>
        
        {/* Footer Info */}
        {!isLoading && filteredTickets.length > 0 && (
          <div className="mt-4 text-xs text-brand-text-muted text-right">
            Showing {filteredTickets.length} tickets
          </div>
        )}
      </div>
    </div>
  );
}
