# -*- coding: utf-8 -*-

# Resolving gettext as _ for module loading.
from gettext import gettext as _

SKILL_NAME = "Gloucester Guide"

WELCOME = _("トグルへようこそ!")
HELP = _("トグルでプロジェクト名のタイトルを開始して，と言ってください．")
STOP = _("終了いたします!")
FALLBACK = _("The {} can't help you with that. ")
SUCCESS_STOP_TIMER = _("タイマーをストップしました．")
FAILURE_STOP_TIMER = _("タイマーのストップに失敗しました．")
NO_TIMER = _("タイマーが開始されていません．")
START_TIMER = _("{0}の{1}を開始します")
NO_PROJECT = _("プロジェクト名がわかりません．")
NOT_PROJECT_NAME = _("{}というプロジェクトは存在しません．")
NO_TITLE = _("タイトルがわかりません．")

NO_DATE_REVIEW = _("日付がわかりません．")
ERROR_REVIEW = _("トグルとの通信に失敗しました．")

CITY_DATA = {
    "city": "Gloucester",
    "state": "MA",
    "postcode": "01930",
    "restaurants": [
        {
            "name": "Zeke's Place",
            "address": '66 East Main Street',
            "phone": '978-283-0474',
            "meals": 'breakfast, lunch',
            "description": 'A cozy and popular spot for breakfast.  Try the blueberry french toast!',
        },
        {
            "name": 'Morning Glory Coffee Shop',
            "address": '25 Western Avenue',
            "phone": '978-281-1851',
            "meals": 'coffee, breakfast, lunch',
            "description": 'A homestyle diner located just across the street from the harbor sea wall.',
        },
        {
            "name": 'Sugar Magnolias',
            "address": '112 Main Street',
            "phone": '978-281-5310',
            "meals": 'breakfast, lunch',
            "description": 'A quaint eatery, popular for weekend brunch.  Try the carrot cake pancakes.',
        },
        {
            "name": 'Seaport Grille',
            "address": '6 Rowe Square',
            "phone": '978-282-9799',
            "meals": 'lunch, dinner',
            "description": 'Serving seafood, steak and casual fare.  Enjoy harbor views on the deck.',
        },
        {
            "name": 'Latitude 43',
            "address": '25 Rogers Street',
            "phone": '978-281-0223',
            "meals": 'lunch, dinner',
            "description": 'Features artsy decor and sushi specials.  Live music evenings at the adjoining Minglewood Tavern.',
        },
        {
            "name": "George's Coffee Shop",
            "address": '178 Washington Street',
            "phone": '978-281-1910',
            "meals": 'coffee, breakfast, lunch',
            "description": 'A highly rated local diner with generously sized plates.',
        },
    ],
    "attractions": [
        {
            "name": 'Whale Watching',
            "description": 'Gloucester has tour boats that depart twice daily from Rogers street at the harbor.  Try either the 7 Seas Whale Watch, or Captain Bill and Sons Whale Watch. ',
            "distance": '0',
        },
        {
            "name": 'Good Harbor Beach',
            "description": 'Facing the Atlantic Ocean, Good Harbor Beach has huge expanses of soft white sand that attracts hundreds of visitors every day during the summer.',
            "distance": '2',
        },
        {
            "name": 'Rockport',
            "description": 'A quaint New England town, Rockport is famous for rocky beaches, seaside parks, lobster fishing boats, and several art studios.',
            "distance": '4',
        },
        {
            "name": 'Fenway Park',
            "description": 'Home of the Boston Red Sox, Fenway park hosts baseball games From April until October, and is open for tours. ',
            "distance": '38',
        },
    ],
}

MY_API = {
    "host": "https://query.yahooapis.com",
    "port": 443,
    "path": "/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22{city}%2C%20{state}%22)&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys",
}
