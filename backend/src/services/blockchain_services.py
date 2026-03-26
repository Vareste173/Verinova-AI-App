from fastapi import APIRouter, Depends, HTTPException
import pandas
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from blockchain.blockchain import Blockchain
from src.database.db_connection import save_dataframe
from pydantic import BaseModel

router = APIRouter()
blockchain = Blockchain()

connection_string = "mysql+pymysql://root:1234@localhost:3306/fintech_db"
engine = create_engine(connection_string)
SessionLocal = sessionmaker(bind=engine)

class TransactionData(BaseModel):
    data: str

@router.post("/transaction")
def add_transaction(data: dict):
    blockchain.add_transaction(data)
    db = SessionLocal()
    try:
        core_df = pandas.DataFrame([{
            "user_id": 1,
            "file_name": "blockchain_tx",
            "file_type": "json"
        }])
        save_dataframe(core_df, "transactions_core", connection_string)
        last_id = db.execute("SELECT LAST_INSERT_ID()").scalar()
        meta_df = pandas.DataFrame([{
            "transaction_id": last_id,
            "meta_key": "transaction",
            "meta_value": str(data)
        }])
        save_dataframe(meta_df, "transactions_metadata", connection_string)
        return {
            "status": "ok",
            "chain_length": len(blockchain.chain),
            "transaction_id": last_id
        }
    finally:
        db.close()

@router.post("/mine_block")
def mine_block(block_data: TransactionData):
    new_block = blockchain.add_block(block_data.data)
    return new_block.__dict__

@router.get("/chain")
def get_chain():
    chain_data = [block.__dict__ for block in blockchain.chain]
    return {"length": len(blockchain.chain), "chain": chain_data}

@router.get("/last_block")
def get_last_block():
    return blockchain.chain[-1].__dict__ if blockchain.chain else {}

@router.get("/validate")
def validate_chain():
    return {"is_valid": blockchain.is_chain_valid()}

