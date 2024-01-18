from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import Column, Integer, String, ForeignKey, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

app = FastAPI()

DATABASE_URL = "sqlite+aiosqlite:///./libraryMS.db" 
engine = create_async_engine(DATABASE_URL)
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Database Models
class Book(Base):
    """Model for representing books in the library."""
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String)

class User(Base):
    """Model for representing users in the library."""
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    transactions = relationship("BookTransaction", back_populates="user")

class BookTransaction(Base):
    """Model for representing book transactions (checkouts) in the library."""
    __tablename__ = "book_transactions"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    checkout_date = Column(String) 
    user = relationship("User", back_populates="transactions")
    book = relationship("Book")


# API endpoints

@app.get("/")
async def read_root():
    """Root endpoint to welcome users."""
    return {"Welcome to": "Library Management System"}


async def get_db():
    """Get a database session for API endpoint."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.commit()
        await db.close()

@app.post("/add_book/")
async def add_book(title: str, author: str, db: AsyncSession = Depends(get_db)):
    """Add a new book to the library."""
    new_book = Book(title=title, author=author)
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    return new_book

@app.put("/edit_book/{book_id}")
async def edit_book(book_id: int, title: str, author: str, db: AsyncSession = Depends(get_db)):
    """Edit details of an existing book."""
    result = await db.execute(select(Book).filter(Book.id == book_id))
    book = result.scalars().first()
    if book:
        book.title = title
        book.author = author
        await db.commit()
        await db.refresh(book)
        return book
    else:
        raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/delete_book/{book_id}")
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a book from the library."""
    result = await db.execute(select(Book).filter(Book.id == book_id))
    print(result)
    book = result.scalars().first()
    if book:
        await db.delete(book)
        await db.commit()
        return {"message": "Book deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Book not found")
    
@app.get("/get_all_books/")
async def get_all_books(db: AsyncSession = Depends(get_db)):
    """Get a list of all books in the library."""
    results = await db.execute(select(Book))
    books = results.scalars().all()
    return books

@app.post("/add_user/")
async def add_user(username: str, db: AsyncSession = Depends(get_db)):
    """Add a new user to the library."""
    new_user = User(username=username)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@app.put("/edit_user/{user_id}")
async def edit_user(user_id: int, username: str, db: AsyncSession = Depends(get_db)):
    """Edit details of an existing user."""
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.username = username
        await db.commit()
        await db.refresh(user)
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.delete("/delete_user/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a user from the library."""
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()    
    if user:
        await db.delete(user)
        await db.commit()
        return {"message": "User deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.get("/get_all_users/")
async def get_all_users(db: AsyncSession = Depends(get_db)):
    """Get a list of all users in the library."""
    results = await db.execute(select(User))
    users = results.scalars().all()
    return users

@app.post("/checkout_book/{user_id}/{book_id}", response_model=None)
async def checkout_book(user_id: int, book_id: int, checkout_date: str, db: AsyncSession = Depends(get_db)):
    """Checkout a book for a user."""
    result_user = await db.execute(select(User).filter(User.id == user_id))
    user = result_user.scalars().first()
    result_book = await db.execute(select(Book).filter(Book.id == book_id))
    book = result_book.scalars().first()

    if user and book:
        new_transaction = BookTransaction(user_id=user_id, book_id=book_id, checkout_date=checkout_date)
        db.add(new_transaction)
        await db.commit()
        await db.refresh(new_transaction)
        return new_transaction
    else:
        raise HTTPException(status_code=404, detail="User or Book not found")

@app.get("/checked_out_users/")
async def checked_out_users(db: AsyncSession = Depends(get_db)):
    """Get a list of users who have checked out books."""
    results = await db.execute(select(BookTransaction))
    transactions = results.scalars().all()
    checked_out_users = [{"user_id": transaction.user_id, "book_id": transaction.book_id, "checkout_date": transaction.checkout_date} for transaction in transactions]
    return checked_out_users


