'use client';

import { useState } from 'react';
import { Ticket } from '@/types';
import { draftTicketAnswer } from '@/lib/api';

interface Props {
  ticket: Ticket;
  onClose: () => void;
}

export default function TicketDetails({ ticket, onClose }: Props) {
  const [draft, setDraft] = useState<string | null>(null);
  const [isDrafting, setIsDrafting] = useState(false);

  const handleDraftAnswer = async () => {
    setIsDrafting(true);
    try {
      const result = await draftTicketAnswer(ticket.id);
      setDraft(result.draft);
    } catch (err) {
      console.error('Failed to draft answer', err);
      alert('Failed to generate draft. Please try again.');
    } finally {
      setIsDrafting(false);
    }
  };

  const formatDate = (dateString: string) => {
    try {
      return new Date(dateString).toLocaleString('en-US', {
        month: 'long',
        day: 'numeric',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      });
    } catch (e) {
      return dateString;
    }
  };

  return (
    <div className="fixed inset-0 bg-black/80 flex items-center justify-center p-4 z-50">
      <div className="card-b2b w-full max-w-2xl p-8 rounded-lg relative overflow-y-auto max-h-[90vh]">
        <button 
          onClick={onClose}
          className="absolute top-4 right-4 text-brand-text-muted hover:text-brand-text text-xl"
        >
          ✕
        </button>
        
        <div className="mb-6">
          <div className="flex items-center gap-3 mb-2">
            <h2 className="text-2xl font-bold text-brand-orange">{ticket.customer_name}</h2>
            <span className="px-2 py-1 bg-brand-gray rounded text-xs text-brand-text-muted">
              {ticket.category}
            </span>
          </div>
          <p className="text-sm text-brand-text-muted">{formatDate(ticket.created_at)}</p>
        </div>

        <div className="mb-8">
          <h3 className="text-xs font-bold uppercase tracking-wider text-brand-text-muted mb-3">Message</h3>
          <div className="bg-brand-gray p-4 rounded border border-brand-gray-light text-brand-text leading-relaxed">
            {ticket.message}
          </div>
        </div>

        <div className="grid grid-cols-2 gap-6 mb-8">
          <div>
            <h3 className="text-xs font-bold uppercase tracking-wider text-brand-text-muted mb-2">Priority</h3>
            <span className={`font-medium ${ticket.priority === 'high' ? 'text-brand-orange' : 'text-brand-text'}`}>
              {ticket.priority.toUpperCase()}
            </span>
          </div>
          <div>
            <h3 className="text-xs font-bold uppercase tracking-wider text-brand-text-muted mb-2">Status</h3>
            <span className={`font-medium ${ticket.status === 'resolved' ? 'text-green-500' : 'text-brand-text'}`}>
              {ticket.status.toUpperCase()}
            </span>
          </div>
        </div>

        <div className="border-t border-brand-gray pt-6">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-bold text-brand-text">AI Draft Response</h3>
            {ticket.status !== 'resolved' && (
              <button
                onClick={handleDraftAnswer}
                disabled={isDrafting}
                className="btn-primary px-4 py-2 rounded text-sm font-medium disabled:opacity-50"
              >
                {isDrafting ? 'Generating...' : 'Draft Answer'}
              </button>
            )}
          </div>

          {draft ? (
            <div className="bg-brand-orange/5 border border-brand-orange/20 p-4 rounded text-brand-text italic leading-relaxed">
              {draft}
            </div>
          ) : (
            ticket.status === 'resolved' ? (
              <p className="text-sm text-brand-text-muted italic">Draft response is not available for resolved tickets.</p>
            ) : (
              <p className="text-sm text-brand-text-muted italic">Click the button above to generate a professional draft response.</p>
            )
          )}
        </div>
      </div>
    </div>
  );
}
