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
    account_index: int = Field(0, ge=0, description="The account index for derivation (e.g., 0 for the first account).")
    change_index: int = Field(0, ge=0, le=1, description="The change index for derivation (0 for receive addresses, 1 for change addresses).")
    address_types: Optional[List[str]] = Field(None, description="List of address types to derive. If empty or None, all supported types for the given xpub will be returned.")

class DeriveAddressesResponse(BaseModel):
    derived_addresses: Dict[str, List[str]] = Field(..., description="An object where keys are address types and values are arrays of derived addresses.")

@app.post("/derive-addresses", response_model=DeriveAddressesResponse)
async def derive_addresses(request: DeriveAddressesRequest):
    derived_addresses = {
        "p2pkh": [],
        "p2sh_segwit": [],
        "bech32": []
    }

    try:
        hd_key = HDKey(request.xpub) # This handles xpub, ypub, zpub prefixes and sets internal state

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
             raise HTTPException(status_code=400, detail="Unsupported xpub type. Must be xpub, ypub, or zpub for implicit address type derivation.")

        # If specific address types are requested, filter them. Otherwise, use the default.
        types_to_derive = request.address_types if request.address_types else [default_address_type]


        for i in range(request.num_addresses):
            # Derivation path: change_index / address_index from the HDKey
            child_key = hd_key.subkey_for_path(f"{request.change_index}/{i}")

            # bitcoinlib's HDKey.address() method will return the appropriate address type
            # based on the initial HDKey's type (xpub, ypub, zpub)
            
            # Populate the list for the default/requested address type
            if default_address_type in types_to_derive:
                 derived_addresses[default_address_type].append(child_key.address())

        # Clean up empty lists and ensure only requested types are returned
        final_derived_addresses = {}
        for k, v in derived_addresses.items():
            if v and (not request.address_types or k in request.address_types):
                final_derived_addresses[k] = v

    except Exception as e:
        print(f"Error during address derivation: {e}") # Log for debugging
        raise HTTPException(status_code=400, detail=f"Error deriving addresses: {str(e)}. Please check your xpub and derivation parameters.")

    return {"derived_addresses": final_derived_addresses}

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host=host, port=port)
