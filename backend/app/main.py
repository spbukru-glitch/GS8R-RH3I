from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import uuid

SECRET_KEY = "splegalmart-dev-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 12

app = FastAPI(title="SpLegalMart API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# -----------------------------
# In-memory demo storage
# -----------------------------
users_db: Dict[str, Dict[str, Any]] = {
    "admin@splegalmart.com": {
        "email": "admin@splegalmart.com",
        "name": "Admin",
        "password_hash": pwd_context.hash("admin123"),
        "role": "admin",
    }
}

services_db: List[Dict[str, Any]] = [
    {"id": "svc-001", "category": "Company formation", "name": "Private Limited Company", "fee": 4999, "unit": "one-time", "description": "Startup incorporation and compliance setup."},
    {"id": "svc-002", "category": "Company formation", "name": "LLP Registration", "fee": 3499, "unit": "one-time", "description": "Simplified partnership setup for founders."},
    {"id": "svc-003", "category": "Legal compliance", "name": "GST Registration", "fee": 2499, "unit": "one-time", "description": "GST setup and filing guidance."},
    {"id": "svc-004", "category": "Legal compliance", "name": "Trademark Filing", "fee": 5999, "unit": "one-time", "description": "Brand protection with legal filing support."},
    {"id": "svc-005", "category": "Legal compliance", "name": "Annual Compliance", "fee": 1999, "unit": "yearly", "description": "Director, secretarial and statutory upkeep."},
    {"id": "svc-006", "category": "Contracts", "name": "Vendor Agreements", "fee": 2999, "unit": "per draft", "description": "Commercial vendor and procurement contracts."},
    {"id": "svc-007", "category": "Contracts", "name": "Employment Agreements", "fee": 1999, "unit": "per draft", "description": "Offer letters, employment terms, and policies."},
    {"id": "svc-008", "category": "Contracts", "name": "MSA & NDA", "fee": 2499, "unit": "per set", "description": "Master service setup and confidentiality terms."},
    {"id": "svc-009", "category": "Disputes", "name": "Legal Notice Drafting", "fee": 1499, "unit": "per notice", "description": "Fast legal notice support and drafting."},
    {"id": "svc-010", "category": "Disputes", "name": "Debt Recovery", "fee": 8999, "unit": "case-based", "description": "Demand, negotiation, and formal recovery support."},
    {"id": "svc-011", "category": "Disputes", "name": "Consumer Complaint", "fee": 2999, "unit": "per case", "description": "Consumer redressal documentation and filing support."},
    {"id": "svc-012", "category": "Property", "name": "Property Due Diligence", "fee": 4999, "unit": "per property", "description": "Title and ownership verification and review."},
    {"id": "svc-013", "category": "Property", "name": "Rent Agreement Review", "fee": 1999, "unit": "per agreement", "description": "Drafting and legal review of lease documents."},
    {"id": "svc-014", "category": "Property", "name": "Sale Deed Assistance", "fee": 8999, "unit": "per transaction", "description": "End-to-end documentation for property transfer."},
    {"id": "svc-015", "category": "IP & Brand", "name": "Copyright Registration", "fee": 3999, "unit": "one-time", "description": "Creative asset protection and filing support."},
    {"id": "svc-016", "category": "IP & Brand", "name": "Design Registration", "fee": 4999, "unit": "one-time", "description": "Industrial design filing and support."},
    {"id": "svc-017", "category": "IP & Brand", "name": "Brand Watch & Enforcement", "fee": 6999, "unit": "monthly", "description": "Monitoring, enforcement, and watch services."},
    {"id": "svc-018", "category": "Startup advisory", "name": "Founder Advisory", "fee": 2999, "unit": "monthly", "description": "Strategic legal guidance for founders and startups."},
    {"id": "svc-019", "category": "Startup advisory", "name": "Shareholder Agreement", "fee": 4999, "unit": "per draft", "description": "Founder rights, obligations, and exit terms."},
    {"id": "svc-020", "category": "Startup advisory", "name": "ESOP Documentation", "fee": 7999, "unit": "per plan", "description": "Employee stock plan documentation and review."},
    {"id": "svc-021", "category": "Documentation", "name": "Will & Estate Planning", "fee": 2999, "unit": "per plan", "description": "Will, trust, and estate legal documentation."},
    {"id": "svc-022", "category": "Documentation", "name": "Power of Attorney", "fee": 1499, "unit": "per assignment", "description": "POA drafting and issuance support."},
    {"id": "svc-023", "category": "Documentation", "name": "Online Legal Audit", "fee": 1999, "unit": "per audit", "description": "Business legal health check and risk review."},
    {"id": "svc-024", "category": "Documentation", "name": "Legal SOPs", "fee": 4999, "unit": "per set", "description": "Internal legal process and workflow design."},
    {"id": "svc-025", "category": "Quick consults", "name": "15-Minute Consultation", "fee": 199, "unit": "per session", "description": "Quick legal answer for urgent questions."},
    {"id": "svc-026", "category": "Quick consults", "name": "Premium Legal Consultation", "fee": 4999, "unit": "per case", "description": "Premium one-to-one advisory for business matters."},
]

bookings_db: List[Dict[str, Any]] = []


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class BookingCreate(BaseModel):
    name: str = Field(..., min_length=2)
    email: str
    phone: str
    city: str
    service: str
    consultation_type: str = "Video Call"
    budget: str = "₹1,000 - ₹5,000"
    message: str = ""
    urgency: str = "This week"


class ServiceItem(BaseModel):
    id: Optional[str] = None
    category: str
    name: str
    fee: int
    unit: str
    description: str


class BookingResponse(BaseModel):
    id: str
    name: str
    email: str
    phone: str
    city: str
    service: str
    consultation_type: str
    budget: str
    message: str
    urgency: str
    status: str
    created_at: str


def create_access_token(email: str) -> str:
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": email, "exp": datetime.utcnow() + expires_delta}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = users_db.get(email)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user


@app.get("/health")
def health():
    return {"status": "ok", "service": "SpLegalMart API"}


@app.post("/api/auth/login", response_model=Token)
def login(payload: UserLogin):
    user = users_db.get(payload.email)
    if not user or not pwd_context.verify(payload.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(user["email"])
    return {"access_token": token, "token_type": "bearer"}


@app.get("/api/me")
def me(current_user: Dict[str, Any] = Depends(get_current_user)):
    return {"email": current_user["email"], "name": current_user["name"], "role": current_user["role"]}


@app.get("/api/services")
def get_services():
    return {"items": services_db}


@app.post("/api/bookings")
def create_booking(payload: BookingCreate):
    booking = {
        "id": f"bk-{uuid.uuid4().hex[:8]}",
        "name": payload.name,
        "email": payload.email,
        "phone": payload.phone,
        "city": payload.city,
        "service": payload.service,
        "consultation_type": payload.consultation_type,
        "budget": payload.budget,
        "message": payload.message,
        "urgency": payload.urgency,
        "status": "New",
        "created_at": datetime.utcnow().isoformat(),
    }
    bookings_db.append(booking)
    return {"success": True, "booking": booking}


@app.get("/api/admin/bookings", response_model=List[BookingResponse])
def list_bookings(current_user: Dict[str, Any] = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    return [BookingResponse(**booking) for booking in bookings_db]


@app.put("/api/admin/bookings/{booking_id}/status")
def update_booking_status(booking_id: str, status: str, current_user: Dict[str, Any] = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")

    for booking in bookings_db:
        if booking["id"] == booking_id:
            booking["status"] = status
            return {"success": True, "booking": booking}

    raise HTTPException(status_code=404, detail="Booking not found")


@app.delete("/api/admin/bookings/{booking_id}")
def delete_booking(booking_id: str, current_user: Dict[str, Any] = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")

    for index, booking in enumerate(bookings_db):
        if booking["id"] == booking_id:
            del bookings_db[index]
            return {"success": True, "deleted": booking_id}

    raise HTTPException(status_code=404, detail="Booking not found")


@app.post("/api/admin/services")
def create_service(payload: ServiceItem, current_user: Dict[str, Any] = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")

    service = payload.model_dump()
    service["id"] = service.get("id") or f"svc-{uuid.uuid4().hex[:6]}"
    services_db.append(service)
    return {"success": True, "service": service}


@app.put("/api/admin/services/{service_id}")
def update_service(service_id: str, payload: ServiceItem, current_user: Dict[str, Any] = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")

    for index, service in enumerate(services_db):
        if service["id"] == service_id:
            updated = payload.model_dump()
            updated["id"] = service_id
            services_db[index] = updated
            return {"success": True, "service": updated}

    raise HTTPException(status_code=404, detail="Service not found")


@app.delete("/api/admin/services/{service_id}")
def delete_service(service_id: str, current_user: Dict[str, Any] = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")

    for index, service in enumerate(services_db):
        if service["id"] == service_id:
            del services_db[index]
            return {"success": True, "deleted": service_id}

    raise HTTPException(status_code=404, detail="Service not found")


@app.get("/api/admin/services")
def admin_services(current_user: Dict[str, Any] = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    return {"items": services_db}
