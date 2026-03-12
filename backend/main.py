from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from pydantic import BaseModel
from contextlib import asynccontextmanager

from database.models import AsyncSessionLocal, Ticket, init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

# Pydantic Schemas
class TicketCreate(BaseModel):
    customer_name: str
    message: str

class TicketUpdate(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None

class TicketResponse(BaseModel):
    id: int
    customer_name: str
    message: str
    status: str
    priority: str
    category: str

    class Config:
        from_attributes = True

# Dependency to get DB session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@app.get("/tickets", response_model=List[TicketResponse])
async def get_tickets(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Ticket))
    tickets = result.scalars().all()
    return tickets

@app.post("/tickets", response_model=TicketResponse)
async def create_ticket(ticket: TicketCreate, db: AsyncSession = Depends(get_db)):
    # Hardcoded values for now as requested
    new_ticket = Ticket(
        customer_name=ticket.customer_name,
        message=ticket.message,
        category="General Support", # Hardcoded
        priority="low"              # Hardcoded
    )
    db.add(new_ticket)
    await db.commit()
    await db.refresh(new_ticket)
    return new_ticket

@app.patch("/tickets/{ticket_id}", response_model=TicketResponse)
async def update_ticket(ticket_id: int, ticket_update: TicketUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Ticket).filter(Ticket.id == ticket_id))
    db_ticket = result.scalar_one_or_none()
    
    if not db_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    if ticket_update.status is not None:
        db_ticket.status = ticket_update.status
    if ticket_update.priority is not None:
        db_ticket.priority = ticket_update.priority
        
    await db.commit()
    await db.refresh(db_ticket)
    return db_ticket
