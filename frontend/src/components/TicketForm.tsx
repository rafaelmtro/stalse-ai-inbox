'use client';

import { useState } from 'react';

interface Props {
  onSubmit: (data: { customer_name: string; message: string }) => Promise<void>;
}

export default function TicketForm({ onSubmit }: Props) {
  const [name, setName] = useState('');
  const [message, setMessage] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim() || !message.trim()) return;

    setIsSubmitting(true);
    try {
      await onSubmit({ customer_name: name, message });
      setName('');
      setMessage('');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="card-b2b p-6 rounded-lg mb-8">
      <h2 className="text-xl font-bold mb-4 text-brand-orange">New Ticket</h2>
      
      <div className="mb-4">
        <label htmlFor="name" className="block text-sm font-medium text-brand-text-muted mb-1">
          Customer Name
        </label>
        <input
          id="name"
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
          className="w-full bg-brand-gray border border-brand-gray-light rounded p-2 text-brand-text focus:outline-none focus:border-brand-orange transition-colors"
          placeholder="Enter customer name..."
        />
      </div>

      <div className="mb-4">
        <label htmlFor="message" className="block text-sm font-medium text-brand-text-muted mb-1">
          Message
        </label>
        <textarea
          id="message"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          required
          rows={4}
          className="w-full bg-brand-gray border border-brand-gray-light rounded p-2 text-brand-text focus:outline-none focus:border-brand-orange transition-colors"
          placeholder="Describe the issue..."
        />
      </div>

      <button
        type="submit"
        disabled={isSubmitting}
        className="btn-primary w-full py-2 rounded font-medium disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {isSubmitting ? 'Submitting...' : 'Submit Ticket'}
      </button>
    </form>
  );
}
