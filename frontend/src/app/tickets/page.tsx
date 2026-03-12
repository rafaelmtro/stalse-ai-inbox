'use client';

import { useState, useEffect } from 'react';
import { Ticket, CreateTicketData } from '@/types';
import { fetchTickets, createTicket, updateTicket } from '@/lib/api';
import TicketItem from '@/components/TicketItem';
import TicketForm from '@/components/TicketForm';

export default function TicketsPage() {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadTickets();
  }, []);

  const loadTickets = async () => {
    try {
      setIsLoading(true);
      const data = await fetchTickets();
      // Sort by priority (high first) and then by id (newest first assuming auto-increment)
      const sorted = data.sort((a, b) => {
        if (a.priority === 'high' && b.priority === 'low') return -1;
        if (a.priority === 'low' && b.priority === 'high') return 1;
        return b.id - a.id;
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
      // Optimistic update
      setTickets((prev) => 
        prev.map(t => t.id === id ? { ...t, status } : t)
      );
      await updateTicket(id, { status });
    } catch (err) {
      console.error('Failed to update status', err);
      // Revert on failure (reload from server is simplest)
      loadTickets();
    }
  };

  const handleUpdatePriority = async (id: number, priority: 'low' | 'high') => {
    try {
      // Optimistic update
      setTickets((prev) => 
        prev.map(t => t.id === id ? { ...t, priority } : t)
      );
      await updateTicket(id, { priority });
    } catch (err) {
      console.error('Failed to update priority', err);
      // Revert on failure
      loadTickets();
    }
  };

  return (
    <div className="min-h-screen bg-brand-black p-4 md:p-8">
      <div className="max-w-4xl mx-auto">
        <header className="mb-8 flex items-center justify-between border-b border-brand-gray pb-4">
          <h1 className="text-3xl font-bold text-brand-text flex items-center gap-2">
            <span className="text-brand-orange">AI</span> Inbox
          </h1>
        </header>

        <main>
          <TicketForm onSubmit={handleCreateTicket} />

          <div className="mt-12">
            <h2 className="text-xl font-bold mb-6 text-brand-text">Recent Tickets</h2>
            
            {error && (
              <div className="p-4 bg-red-900/50 border border-red-500 rounded text-red-200 mb-6">
                {error}
              </div>
            )}

            {isLoading ? (
              <div className="text-center py-12 text-brand-text-muted">Loading tickets...</div>
            ) : tickets.length === 0 ? (
              <div className="text-center py-12 text-brand-text-muted border border-dashed border-brand-gray rounded-lg">
                No tickets found. Create one above.
              </div>
            ) : (
              <div className="flex flex-col gap-2">
                {tickets.map((ticket) => (
                  <TicketItem
                    key={ticket.id}
                    ticket={ticket}
                    onUpdateStatus={handleUpdateStatus}
                    onUpdatePriority={handleUpdatePriority}
                  />
                ))}
              </div>
            )}
          </div>
        </main>
      </div>
    </div>
  );
}
