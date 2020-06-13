#copyright (c)2020 #artadi All rights reserved

#pk_5f1a794f08884efa8addfcc924e49846
from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages

import requests
import json

def home(request):

	if request.method == "POST":
		ticker = request.POST['ticker_symbol']
		api_request = requests.get("https://cloud.iexapis.com/stable/stock/"+ticker+"/quote?token=pk_5f1a794f08884efa8addfcc924e49846")
	
		try:
			api = json.loads(api_request.content)
		except Exception as e:
			api = "Error..."
		return render(request, 'home.html', {'api': api})

	else:
		return render(request, 'home.html', {'ticker': "Enter the symbol above..."})



def about(request):
	return render(request, 'about.html', {})

def add_stock(request):
	if request.method == "POST":
		form = StockForm(request.POST or None)

		if form.is_valid():
			form.save()
			messages.success(request,('stock has been added'))
			return redirect('add_stock')

	else:
		tiker = Stock.objects.all()
		output = []
		for ticker_item in tiker:
			api_request = requests.get("https://cloud.iexapis.com/stable/stock/"+str(ticker_item)+"/quote?token=pk_5f1a794f08884efa8addfcc924e49846")
			try:
				api = json.loads(api_request.content)
				output.append(api)
			except Exception as e:
				api = "Error..."

		return render(request, 'add_stock.html', {'tiker':tiker, 'output': output})

def delete(request, stock_id):
	item = Stock.objects.get(pk=stock_id)
	item.delete()
	messages.success(request, ('Stock has been deleted'))
	return redirect (delete_stock)


def delete_stock(request):
	tiker = Stock.objects.all()
	return render(request, 'delete_stock.html', {'tiker':tiker})