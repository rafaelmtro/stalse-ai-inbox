import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import TicketForm from '@/components/TicketForm';

describe('TicketForm', () => {
  it('renders correctly', () => {
    render(<TicketForm onSubmit={jest.fn()} />);
    expect(screen.getByLabelText(/Customer Name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Message/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Submit Ticket/i })).toBeInTheDocument();
  });

  it('submits form with correct data and clears inputs', async () => {
    const mockOnSubmit = jest.fn().mockResolvedValue(undefined);
    render(<TicketForm onSubmit={mockOnSubmit} />);
    
    const nameInput = screen.getByLabelText(/Customer Name/i);
    const messageInput = screen.getByLabelText(/Message/i);
    const submitButton = screen.getByRole('button', { name: /Submit Ticket/i });

    fireEvent.change(nameInput, { target: { value: 'Jane Smith' } });
    fireEvent.change(messageInput, { target: { value: 'Billing question' } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith({
        customer_name: 'Jane Smith',
        message: 'Billing question'
      });
    });

    // Inputs should be cleared after successful submission
    expect(nameInput).toHaveValue('');
    expect(messageInput).toHaveValue('');
  });
});
