#%%
class ElectricityRecord:
    def __init__(self, region, area, year, month, dwelling_type, avg_kwh_per_acc):
        self.region = region
        self.area = area
        self.year = int(year)
        self.month = month
        self.dwelling_type = dwelling_type
        self.avg_kwh_per_acc = avg_kwh_per_acc
    
    
    def __repr__(self):
        """Detailed format for debugging"""
        return (f"ElectricityRecord(region='{self.region}', "
                f"area='{self.area}', "
                f"year={self.year}, "
                f"month={self.month}, "
                f"dwelling_type='{self.dwelling_type}', "
                f"avg_kwh_per_acc={self.avg_kwh_per_acc})")
# %%
