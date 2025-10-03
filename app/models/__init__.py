from ..extensions import db
from datetime import datetime

# Import models in order of dependencies
from . import school  # Base model without dependencies
from . import user   # Depends on school

# Rest of the models that may depend on school and user
from . import (
    challenge,
    lesson,
    badge,
    gamification,
    achievement,
    analytics,
    eco_impact,
    learning,
    social
)