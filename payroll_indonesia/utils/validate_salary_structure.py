def validate_salary_structure_required_components(doc, method):
    import frappe
    
    earning_names = [e.salary_component for e in getattr(doc, "earnings", [])]
    deduction_names = [d.salary_component for d in getattr(doc, "deductions", [])]
    
    missing_components = []
    
    # Komponen BPJS bersifat opsional. Tidak memaksa pasangan employer/employee,
    # sehingga Salary Structure bisa dibuat secara parsial sesuai kebutuhan.
    
    # Validasi PPh 21 - hanya jika ada komponen taxable
    has_taxable = any(
        e.salary_component for e in getattr(doc, "earnings", [])
    )
    if has_taxable:
        if "Biaya Jabatan" not in deduction_names:
            missing_components.append("Biaya Jabatan")
        if "PPh 21" not in deduction_names:
            missing_components.append("PPh 21")
    
    if missing_components:
        frappe.throw(
            "Salary Structure tidak lengkap. Komponen berikut wajib ada:\n- "
            + "\n- ".join(missing_components)
        )
