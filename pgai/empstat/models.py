from django.db import models

# Create your models here.


class Employee(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=50)
    salary = models.IntegerField()

    def __str__(self):
        return self.name
    
class Fuelconsumption(models.Model):
    modelyear = models.IntegerField()
    make = models.CharField(max_length=20)
    model = models.CharField(max_length=50)
    vehicleclass = models.CharField(max_length=25)
    enginesize = models.DecimalField(max_digits=10,decimal_places=1)
    cylinders = models.IntegerField()
    transmission = models.CharField(max_length=5)
    fueltype = models.CharField(max_length=1)
    fuelconsumption_city = models.DecimalField(max_digits=90,decimal_places=2)
    fuelconsumption_hwy = models.DecimalField(max_digits=90,decimal_places=2)
    fuelconsumption_comb = models.DecimalField(max_digits=90,decimal_places=2)
    fuelconsumption_comb_mpg = models.IntegerField()
    co2emissions = models.IntegerField()

    def __str__(self):
        return self.model
    

class WeatherData(models.Model):
    Precipitation = models.DecimalField(max_digits=5, decimal_places=2)
    Date_Full = models.DateField()
    Station_City = models.CharField(max_length=255)
    Station_Code = models.CharField(max_length=255)
    Station_Location = models.CharField(max_length=255)
    Station_State = models.CharField(max_length=255)
    Temperature_Avg = models.DecimalField(max_digits=5, decimal_places=2)
    Temperature_Max = models.DecimalField(max_digits=5, decimal_places=2)
    Temperature_Min = models.DecimalField(max_digits=5, decimal_places=2)
    Wind_Direction = models.CharField(max_length=255)
    Wind_Speed = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.Date_Full} - {self.Station_Location}"

    class Meta:
        verbose_name_plural = "Weather Data"

class Sales(models.Model):
    ordernumber = models.IntegerField()
    quantityordered = models.IntegerField()
    priceeach = models.DecimalField(max_digits=5, decimal_places=2)
    # orderlinenumber = models.IntegerField()
    sales = models.DecimalField(max_digits=10, decimal_places=2)
    orderdate = models.DateField()
    status = models.CharField(max_length=25)
    # qtr_id = models.IntegerField()
    # month_id = models.IntegerField()
    year_id = models.IntegerField()
    productline = models.CharField(max_length=25)
    msrp = models.IntegerField()
    productcode = models.CharField(max_length=10)
    customername = models.TextField()
    city = models.CharField(max_length=25)
    # state = models.CharField(max_length=25, null= True)
    country = models.CharField(max_length=25)
    contactlastname = models.CharField(max_length=25)
    contactfirstname = models.CharField(max_length=25)
    dealsize = models.CharField(max_length=10)

    def __str__(self):
        return self.ordernumber

    class Meta:
        verbose_name_plural = "Sales data"