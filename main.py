import rumps
import requests
import json

API_URL = 'https://koinex.in/api/ticker'

UPDATE_INTERVAL = 60

CURRENCIES = {
    'Bitcoin': 'BTC',
    'Ethereum': 'ETH',
    'Ripple': 'XRP',
    'Litecoin': 'LTC',
    'Bitcoin Cash': 'BCH',
}


class KoinexStatusBarApp(rumps.App):
    def __init__(self):
        super(KoinexStatusBarApp, self).__init__("Koinex")
        self.currencies = CURRENCIES.keys()
        self.menu = CURRENCIES.keys()
        self.enabled = ['Bitcoin', 'Ripple']
        self.prices = {}

        # Initialize click handlers
        for item in self.menu:
            rumps.clicked(item)(self.toggle_currency)

        # Add check to menu items which are enabled
        for item in self.enabled:
            self.menu[item].state = 1

        # Add separator
        self.menu.add(None)

    @rumps.timer(UPDATE_INTERVAL)
    def update(self, sender):
        response = requests.get(API_URL)
        title = ''
        if response.status_code == 200:
            data = json.loads(response.content)
            self.prices = data.get('prices', {})

        for currency in self.enabled:
            short = CURRENCIES.get(currency)
            title += u'{} \u20B9 {} | '.format(short, self.prices.get(short))
        self.title = title[:-3] # Last 3 characters will be ' | '

    def toggle_currency(self, menuitem):
        currency = menuitem.title
        if currency in self.enabled:
            self.enabled.remove(currency)
            menuitem.state = 0
        else:
            self.enabled.append(currency)
            menuitem.state = 1
        self.update(None)


if __name__ == "__main__":
    KoinexStatusBarApp().run()