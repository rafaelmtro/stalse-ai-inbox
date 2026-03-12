import { render, screen, fireEvent } from '@testing-library/react';
import TicketItem from '@/components/TicketItem';
import { Ticket } from '@/types';

const mockTicket: Ticket = {
  id: 1,
  customer_name: 'John Doe',
  message: 'My system is crashing',
  status: 'pending',
  priority: 'high',
  category: 'Technical Support'
};

describe('TicketItem', () => {
  it('renders ticket details correctly', () => {
    render(<TicketItem ticket={mockTicket} onUpdateStatus={jest.fn()} onUpdatePriority={jest.fn()} />);
    
    expect(screen.getByText('John Doe')).toBeInTheDocument();
    expect(screen.getByText('My system is crashing')).toBeInTheDocument();
    expect(screen.getByText('Technical Support')).toBeInTheDocument();
  });

  it('calls onUpdateStatus when status is changed', () => {
    const mockUpdateStatus = jest.fn();
    render(<TicketItem ticket={mockTicket} onUpdateStatus={mockUpdateStatus} onUpdatePriority={jest.fn()} />);
    
    const statusSelect = screen.getByDisplayValue('Pending');
    fireEvent.change(statusSelect, { target: { value: 'resolved' } });
    
    expect(mockUpdateStatus).toHaveBeenCalledWith(1, 'resolved');
  });

  it('calls onUpdatePriority when priority is changed', () => {
    const mockUpdatePriority = jest.fn();
    render(<TicketItem ticket={mockTicket} onUpdateStatus={jest.fn()} onUpdatePriority={mockUpdatePriority} />);
    
    const prioritySelect = screen.getByDisplayValue('High');
    fireEvent.change(prioritySelect, { target: { value: 'low' } });
    
    expect(mockUpdatePriority).toHaveBeenCalledWith(1, 'low');
  });
});
