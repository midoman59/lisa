# PostgreSQL Configuration - Lisa CreditMe

## Connection Details

| Property | Value |
|----------|-------|
| **Server** | bddlisacreditme.postgres.database.azure.com |
| **Port** | 5432 |
| **Admin User** | adminlisacreditme |
| **Admin Password** | RbsLis@123 |
| **Location** | francecentral |
| **Type** | PostgreSQL Flexible Server |

---

## Connection String

### Standard PostgreSQL Connection String
```
postgresql://adminlisacreditme:RbsLis@123@bddlisacreditme.postgres.database.azure.com:5432/postgres
```

### For Python (psycopg2)
```python
import psycopg2

conn = psycopg2.connect(
    host="bddlisacreditme.postgres.database.azure.com",
    port=5432,
    database="postgres",
    user="adminlisacreditme",
    password="RbsLis@123"
)
```

### For SQLAlchemy (Python ORM)
```python
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg2://adminlisacreditme:RbsLis@123@bddlisacreditme.postgres.database.azure.com:5432/postgres"
)
```

---

## Existing Databases

```
- azure_maintenance (system)
- postgres (default)
- azure_sys (system)
```

**You should create your own database for the app:**

```sql
-- Connect to postgres first, then:
CREATE DATABASE lisa_creditme_app;
```

---

## Security Notes

⚠️ **IMPORTANT:**
1. This password should be in `.env` (not committed to GitHub)
2. Consider using Azure Key Vault in production
3. Firewall rules may need to be configured to allow your IP
4. For production: use strong passwords and limit access

---

## Testing Connection

### Via Command Line
```bash
psql -h bddlisacreditme.postgres.database.azure.com \
     -U adminlisacreditme \
     -d postgres
# Then enter password: RbsLis@123
```

### Via Python
```bash
pip install psycopg2-binary
python -c "
import psycopg2
conn = psycopg2.connect('postgresql://adminlisacreditme:RbsLis@123@bddlisacreditme.postgres.database.azure.com:5432/postgres')
print('Connected!')
conn.close()
"
```

---

## Next Steps

1. Create app database: `CREATE DATABASE lisa_creditme_app;`
2. Create tables for your use case
3. Add connection string to `.env`
