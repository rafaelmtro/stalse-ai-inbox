'use client';

import { Ticket } from '@/types';

interface Props {
  ticket: Ticket;
  onUpdateStatus: (id: number, status: 'pending' | 'resolved') => void;
  onUpdatePriority: (id: number, priority: 'low' | 'high') => void;
}

export default function TicketItem({ ticket, onUpdateStatus, onUpdatePriority }: Props) {
  return (
    <div className="card-b2b p-4 rounded-lg mb-4 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
      <div className="flex-1">
        <div className="flex items-center gap-2 mb-2">
          <h3 className="text-lg font-bold text-brand-text">{ticket.customer_name}</h3>
          <span className="text-xs px-2 py-1 bg-brand-gray rounded text-brand-text-muted">
            {ticket.category}
          </span>
        </div>
        <p className="text-brand-text-muted mb-2">{ticket.message}</p>
      </div>
      
      <div className="flex flex-col gap-2 min-w-[120px]">
        <div className="flex items-center justify-between">
          <label className="text-xs text-brand-text-muted mr-2">Priority:</label>
          <select 
            value={ticket.priority}
            onChange={(e) => onUpdatePriority(ticket.id, e.target.value as 'low' | 'high')}
            className={`text-xs p-1 rounded bg-brand-gray border border-brand-gray-light cursor-pointer
              ${ticket.priority === 'high' ? 'text-brand-orange' : 'text-brand-text'}`}
          >
            <option value="low">Low</option>
            <option value="high">High</option>
          </select>
        </div>
        
        <div className="flex items-center justify-between">
          <label className="text-xs text-brand-text-muted mr-2">Status:</label>
          <select 
            value={ticket.status}
            onChange={(e) => onUpdateStatus(ticket.id, e.target.value as 'pending' | 'resolved')}
            className={`text-xs p-1 rounded bg-brand-gray border border-brand-gray-light cursor-pointer
              ${ticket.status === 'resolved' ? 'text-green-500' : 'text-brand-text'}`}
          >
            <option value="pending">Pending</option>
            <option value="resolved">Resolved</option>
          </select>
        </div>
      </div>
    </div>
  );
}
