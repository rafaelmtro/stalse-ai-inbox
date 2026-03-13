'use client';

import { useState } from 'react';

interface Props {
  onSubmit: (data: { customer_name: string; message: string }) => Promise<void>;
  onClose: () => void;
}

export default function TicketForm({ onSubmit, onClose }: Props) {
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
      onClose();
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/80 flex items-center justify-center p-4 z-50">
      <div className="card-b2b w-full max-w-md p-6 rounded-lg relative">
        <button 
          onClick={onClose}
          className="absolute top-4 right-4 text-brand-text-muted hover:text-brand-text"
        >
          ✕
        </button>
        
        <h2 className="text-xl font-bold mb-6 text-brand-orange">New Ticket</h2>
        
        <form onSubmit={handleSubmit}>
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

          <div className="mb-6">
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

          <div className="flex gap-3">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 py-2 rounded font-medium bg-brand-gray border border-brand-gray-light hover:bg-brand-gray-light transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isSubmitting}
              className="flex-1 btn-primary py-2 rounded font-medium disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isSubmitting ? 'Submitting...' : 'Submit Ticket'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
