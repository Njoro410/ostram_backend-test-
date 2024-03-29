

GENDER_CHOICES = (
    ('MALE', 'Male'),
    ('FEMALE', 'Female')
)

RELATIONSHIP_STATUS_CHOICES = (
    ('single', 'Single'),
    ('married', 'Married')
)

EDUCATIONAL_STATUS_CHOICES = (
    ('Graduate', 'Graduate'),
    ('High School', 'High School'),
    ('Phd', 'Phd'),
    ('Masters', 'Masters'),
)

RESIDENTIAL_STATUS_CHOICES = (
    ('Owner', 'Owner'),
    ('Renting', 'Renting'),
    ('Staying with Parent', 'Staying with Parent'),
)

TITLE_CHOICES = (
    ('MR', 'Mr.'),
    ('MRS', 'Mrs.'),
    ('MS', 'Ms.'),
)

PAYMENT_FREQUENCY_CHOICES = (
    ('daily', 'daily'),
    ('monthly', 'monthly'),
    ('quaterly', 'quaterly'),
    ('bi-annual', 'bi-annual'),
    ('yearly', 'yearly'),
)

STATUS_CHOICES = (
    ('submitted', 'submitted'),
    ('in review', 'in review'),
    ('Open', 'Open'),
    ('Closed', 'Closed'),
)

PAYMENT_METHOD = (
    ('Cash', 'Cash'),
    ('Bank', 'Bank'),
)

MESSAGE_STATUS = (
    ('sent', 'sent'),
    ('received', 'received'),
)

INTEREST_TYPE_CHOICES = (
    ('Simple', 'Simple'),
    ('Compounding', 'Compounding'),
)

DOCUMENT_TYPE_CHOICES = (
    ('National ID', 'National ID'),
    ('Passport', 'Passport'),
    ('KRA Pin', 'KRA Pin'),
    ('Drivers License', 'Drivers License'),
)


ROLES = (
        ('Admin', 'Admin'),
        ('User', 'User'),
)

LOAN_STATUS_CHOICES = (
    ('APPROVED', 'Approved'),
    ('DENIED', 'Denied'),
    ('PENDING', 'Pending'),
    ('IN_PROGRESS', 'In Progress'),
    ('DISBURSED', 'Disbursed'),
    ('REPAID', 'Repaid'),
    ('DEFAULT', 'Default'),
    ('CLOSED', 'Closed'),
    ('CANCELLED', 'Cancelled'),
    ('ON_HOLD', 'On Hold'),
)

DOCUMENT_STATUS_CHOICES = (
    ('ACCEPTED', 'Accepted'),
    ('REJECTED', 'Rejected'),
    ('PENDING', 'Pending'),
)


BRANCH_STATUS_CHOICES = (
    ('ACTIVE', 'Active'),
    ('INACTIVE', 'Inactive'),
)
