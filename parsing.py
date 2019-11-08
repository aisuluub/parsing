from bs4 import BeautifulSoup
import requests
import csv

def get_html(url):
	r = requests.get(url)
	return r.text


def get_total_pages(html):
	soup = BeautifulSoup(html, 'lxml')

	pages = soup.find('ul', class_ = 'pagn').find_all('li',class_= 'pagn-last')[-1].find('a').get('href')
	total_pages = pages.split('=')[-1]

	return int(total_pages)


def write_csv(data):
	with open('lalafo.csv', 'a') as f:
		writer = csv.writer(f)

		writer.writerow( (data['title'], data['price'], data['photo'], data['url'] ) )




def get_page_data(html):
	soup = BeautifulSoup(html, 'lxml')

	ads = soup.find('div', class_ = 'mr-3').find_all('article', class_ = 'listing-item')

	for ad in ads:
		try:
			title = ad.find('div', class_ = 'listing-item-main').find('a', class_='listing-item-title').text.strip()
		except:
			title = ''
		try:
			url = 'https://lalafo.kg'+ad.find('div', class_ = 'listing-item-main').find('a', class_ = 'listing-item-title').get('href')
		except:
			url = ''
		try:
			price = ad.find('div', class_ = 'listing-item-main').find('p', class_ = 'listing-item-title').text.strip()
		except:
			price = ''
		try:
			photo = ad.find('div', class_ = 'listing-item-img-wrap').find('img', class_ = 'listing-item-photo').get('src')
		except:
			photo = ''
		
		data = {'title': title, 'price': price, 'photo': photo, 'url': url }

		write_csv(data)



def main():
	url = 'https://lalafo.kg/kyrgyzstan/mobilnye-telefony-i-aksessuary/mobilnye-telefony?page=1'
	base_url = 'https://lalafo.kg/kyrgyzstan/mobilnye-telefony-i-aksessuary/mobilnye-telefony?'
	pages_part = 'page=' 
	pages = get_total_pages(get_html(url))
	

	total_pages = get_total_pages(get_html(url))

	for i in range(1, total_pages):
		url_gen = base_url + pages_part + str(i)
		#print(url_gen) 
		html = get_html(url_gen)
		get_page_data(html)
		


if __name__ == '__main__':
	main()
