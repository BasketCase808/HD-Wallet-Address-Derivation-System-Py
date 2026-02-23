# bitcoin-derivation-service/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from dotenv import load_dotenv
import os
import uvicorn
from bitcoinlib.keys import HDKey

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Bitcoin Address Derivation Service",
    description="API for deterministic Bitcoin address derivation from Master Public Keys (xpub, ypub, zpub).",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

class DeriveAddressesRequest(BaseModel):
    xpub: str = Field(..., description="The master public key (xpub, ypub, or zpub) from which to derive addresses.")
    num_addresses: int = Field(20, ge=1, le=100, description="The number of addresses to derive.")
    account_index: int = Field(0, ge=0, description="The starting account index for derivation.")
    derivation_index: int = Field(0, ge=0, description="The address index within each account (usually 0).")
    address_types: Optional[List[str]] = Field(None, description="List of address types to derive.")

class DeriveAddressesResponse(BaseModel):
    derived_addresses: Dict[str, List[str]] = Field(..., description="Derived addresses grouped by type.")

@app.post("/derive-addresses", response_model=DeriveAddressesResponse)
async def derive_addresses(request: DeriveAddressesRequest):
    derived_addresses = {
        "p2pkh": [],
        "p2sh_segwit": [],
        "bech32": []
    }

    try:
        hd_key = HDKey(request.xpub)

        # Determine the default address type based on the xpub prefix
        xpub_prefix = request.xpub[:4]
        default_address_type = None
        if xpub_prefix == 'xpub':
            default_address_type = 'p2pkh'
        elif xpub_prefix == 'ypub':
            default_address_type = 'p2sh_segwit'
        elif xpub_prefix == 'zpub':
            default_address_type = 'bech32'

        if not default_address_type:
             raise HTTPException(status_code=400, detail="Unsupported xpub type.")

        types_to_derive = request.address_types if request.address_types else [default_address_type]

        # Iterate through account indices
        for i in range(request.account_index, request.account_index + request.num_addresses):
            # Path: account / change / address_index
            path = f"{i}/{request.derivation_index}"
            child_key = hd_key.subkey_for_path(path)

            if default_address_type in types_to_derive:
                 derived_addresses[default_address_type].append(child_key.address())

        final_derived_addresses = {k: v for k, v in derived_addresses.items() if v}

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

    return {"derived_addresses": final_derived_addresses}

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host=host, port=port)
