export interface Ticket {
  id: number;
  customer_name: string;
  message: string;
  status: 'pending' | 'resolved';
  priority: 'low' | 'high';
  category: string;
}

export interface CreateTicketData {
  customer_name: string;
  message: string;
}

export interface UpdateTicketData {
  status?: 'pending' | 'resolved';
  priority?: 'low' | 'high';
}
