from pydantic import Field, field_validator, BaseModel


#модель для описания операций с деньгами
class OperationRequest(BaseModel):
    wallet_name: str = Field(..., max_length=127)
    amount: float
    description: str | None = Field(None, max_length=255)

    @field_validator('amount')
    def amount_must_be_positive(cls, v:float) -> float:
        if v <= 0:
            raise ValueError('amount must be positive')
        return v

    @field_validator('wallet_name')
    def wallet_name_not_empty(cls, v: str) -> str:
        v = v.strip()
        if v == '':
            raise ValueError("Wallet name can't be empty")
        return v


#модель для описания создания кошелька
class CreateWalletRequests(BaseModel):
    name: str = Field(..., max_length=127)
    initial_balance: float = 0

    @field_validator('name')
    def name_not_empty(cls, v: str) -> str:
        v = v.strip()
        if v == '':
            raise ValueError("Wallet name cannot be empty")
        return v

    @field_validator('initial_balance')
    def balance_not_negative(cls, v: float) -> float:
        if v < 0:
            raise ValueError('initial balance cannot be negative')
        return v