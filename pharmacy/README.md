# Pharmacy App
Функції:
- облік лікарських засобів
- партії та терміни придатності
- продаж за принципом FEFO
- SQLite
- GUI на Tkinter/ttk

pharmacy_app/
│
├── main.py
├── config.py
├── README.md
│
├── database/
│   ├── __init__.py
│   ├── connection.py
│   └── schema.py
│
├── models/
│   ├── __init__.py
│   ├── medicine.py=
│   ├── batch.py=
│   ├── customer.py=
│   ├── supplier.py=
│   ├── category.py=
│   ├── user.py
│   └── sale.py
│
├── repositories/
│   ├── __init__.py
│   ├── medicine_repo.py
│   ├── batch_repo.py
│   ├── customer_repo.py
│   ├── supplier_repo.py
│   ├── user_repo.py
│   └── sale_repo.py
│
services/
├── sales_service.py
├── inventory_service.py
├── medicine_service.py
├── customer_service.py
├── auth_service.py
└── reports_service.py
│
└── gui/
    ├── __init__.py
    ├── app.py
    ├── views/
    │   ├── __init__.py
    │   ├── medicines_view.py
    │   ├── batches_view.py
    │   ├── sales_view.py
    │   └── reports_view.py
    └── widgets/
        ├── __init__.py
        └── forms.py