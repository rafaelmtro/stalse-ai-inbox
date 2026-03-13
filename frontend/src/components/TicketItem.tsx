'use client';

import { Ticket } from '@/types';

interface Props {
  ticket: Ticket;
  onUpdateStatus: (id: number, status: 'pending' | 'resolved') => void;
  onUpdatePriority: (id: number, priority: 'low' | 'high') => void;
  onClick: (ticket: Ticket) => void;
}

export default function TicketItem({ ticket, onUpdateStatus, onUpdatePriority, onClick }: Props) {
  const formatDate = (dateString: string) => {
    try {
      const date = new Date(dateString);
      const mm = String(date.getMonth() + 1).padStart(2, '0');
      const dd = String(date.getDate()).padStart(2, '0');
      const yyyy = date.getFullYear();
      return `${mm}/${dd}/${yyyy}`;
    } catch (e) {
      return dateString;
    }
  };

  return (
    <tr 
      onClick={() => onClick(ticket)}
      className="border-b border-brand-gray hover:bg-brand-gray-light/30 transition-all duration-200 text-sm cursor-pointer group"
    >
      <td className="py-4 px-4 text-brand-text-muted whitespace-nowrap">
        {formatDate(ticket.created_at)}
      </td>
      <td className="py-4 px-2 font-medium text-brand-text whitespace-nowrap">
        {ticket.customer_name}
      </td>
      <td className="py-4 px-2 text-brand-text-muted max-w-xs truncate" title={ticket.message}>
        {ticket.message}
      </td>
      <td className="py-4 px-2">
        <span className="px-2 py-1 bg-brand-gray rounded text-xs text-brand-text-muted">
          {ticket.category}
        </span>
      </td>
      <td className="py-4 px-2" onClick={(e) => e.stopPropagation()}>
        <select 
          value={ticket.priority}
          onChange={(e) => onUpdatePriority(ticket.id, e.target.value as 'low' | 'high')}
          className={`text-xs p-1 rounded bg-brand-gray border border-brand-gray-light cursor-pointer focus:outline-none focus:border-brand-orange
            ${ticket.priority === 'high' ? 'text-brand-orange' : 'text-brand-text'}`}
        >
          <option value="low">Low</option>
          <option value="high">High</option>
        </select>
      </td>
      <td className="py-4 px-2 text-right" onClick={(e) => e.stopPropagation()}>
        <select 
          value={ticket.status}
          onChange={(e) => onUpdateStatus(ticket.id, e.target.value as 'pending' | 'resolved')}
          className={`text-xs p-1 rounded bg-brand-gray border border-brand-gray-light cursor-pointer focus:outline-none focus:border-brand-orange
            ${ticket.status === 'resolved' ? 'text-green-500' : 'text-brand-text'}`}
        >
          <option value="pending">Pending</option>
          <option value="resolved">Resolved</option>
        </select>
      </td>
    </tr>
  );
}
