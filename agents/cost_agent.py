def estimate(team_size, weeks, hourly_rate, contingency_pct, monthly_cloud, cloud_months):
    if team_size < 1 or weeks < 1 or min(hourly_rate, contingency_pct, monthly_cloud, cloud_months) < 0:
        raise ValueError("Team size and weeks must be positive; other inputs cannot be negative.")
    hours = team_size * weeks * 40
    labor = hours * hourly_rate
    cloud = monthly_cloud * cloud_months
    subtotal = labor + cloud
    contingency = subtotal * contingency_pct / 100
    return {
        "engineering_hours": hours, "labor_cost": round(labor, 2),
        "cloud_cost": round(cloud, 2), "subtotal": round(subtotal, 2),
        "contingency": round(contingency, 2), "total": round(subtotal + contingency, 2),
        "currency": "USD",
        "disclaimer": "Illustrative planning estimate only; validate scope, rates, and vendor pricing."
    }
