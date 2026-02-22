import enum

class BookingStatus(str, enum.Enum):
    CONFIRMED = "Confirmed"
    CANCELLED = "Cancelled"
    PENDING = "Pending"

class SessionStatus(str, enum.Enum):
    PLANNED = "Planned"
    ACTIVE = "Active"
    FINISHED = "Finished"
    CANCELLED = "Cancelled"
