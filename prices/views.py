import io,xlsxwriter

from django.http import HttpResponse
from django.shortcuts import render

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .models import AluminiumPrice, PVCPrice


def index(request):
    def parse_stock1():
        driver = webdriver.Firefox()
        driver.get("https://www.investing.com/commodities/aluminum")

        try:
            aluminium_price_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[1]/div[2]/div[3]/div[1]/div[1]/div[3]/div/div[1]/div[1]/div[1]'))
            )

            aluminium_price = aluminium_price_element.text
            print("Aluminum Price:", aluminium_price)
        except Exception as e:
            print("Error:", e)
        return aluminium_price

    def parse_stock2():
        driver = webdriver.Firefox()
        driver.get("https://www.investing.com/commodities/pvc-com-futures")

        try:
            pvc_futures_price_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[1]/div[2]/div[3]/div[1]/div[1]/div[3]/div/div[1]/div[1]/div[1]'))
            )

            pvc_futures_price = pvc_futures_price_element.text
            print("Pvs_future_price:", pvc_futures_price)
        except Exception as e:
            print("Error:", e)
        return pvc_futures_price

    aluminium_price = parse_stock1()
    aluminium_instance = AluminiumPrice(aluminium_price=aluminium_price)
    aluminium_instance.save()
    pvc_futures_price = parse_stock2()
    pvc_instance= PVCPrice(pvc_futures_price=pvc_futures_price)
    pvc_instance.save()

    stock1 = AluminiumPrice.objects.all()
    print(stock1)
    stock2 = PVCPrice.objects.all()
    print(stock2)
    combined_data = [{"alumin": alumin, "pvc": pvc} for alumin, pvc in zip(stock1, stock2)]
    print(combined_data)
    return render(request, "interface.html", {"combined_data": combined_data})


def download_prices_excel(request):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()

    headers = ['Aluminium Price', 'Last Time (Aluminium)', 'PVC Futures Price', 'Last Time (PVC)']

    for col_num, header in enumerate(headers):
        worksheet.write(0, col_num, header)

    aluminium_prices = AluminiumPrice.objects.all()
    pvc_prices = PVCPrice.objects.all()

    for row_num, (aluminium, pvc) in enumerate(zip(aluminium_prices, pvc_prices), start=1):
        worksheet.write(row_num, 0, aluminium.aluminium_price)
        worksheet.write(row_num, 1, aluminium.last_time.strftime('%Y-%m-%d %H:%M:%S'))
        worksheet.write(row_num, 2, pvc.pvc_futures_price)
        worksheet.write(row_num, 3, pvc.last_time.strftime('%Y-%m-%d %H:%M:%S'))

    workbook.close()
    output.seek(0)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=prices.xlsx'
    response.write(output.read())

    return response
